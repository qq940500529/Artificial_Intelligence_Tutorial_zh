window.addEventListener("DOMContentLoaded", () => {
    const graphData = window.GRAPH_DATA;

    if (!graphData || !Array.isArray(graphData.nodes) || !Array.isArray(graphData.edges)) {
        throw new Error("GRAPH_DATA 不存在或格式不正确");
    }

    const svg = d3.select("#knowledge-graph");
    const searchInput = document.getElementById("graph-search");
    const searchResults = document.getElementById("search-results");
    const infoPanel = document.getElementById("info-panel");
    const tooltip = document.getElementById("node-tooltip");
    const resetViewButton = document.getElementById("btn-reset-view");

    const stageColors = graphData.stageColors;
    const nodesById = new Map(graphData.nodes.map((node) => [node.id, node]));
    const childrenById = new Map(graphData.nodes.map((node) => [node.id, []]));
    const incomingById = new Map(graphData.nodes.map((node) => [node.id, []]));
    const outgoingById = new Map(graphData.nodes.map((node) => [node.id, []]));
    const coreStageIds = ["01", "02", "03", "04"].filter((id) => nodesById.has(id));
    const coreStageIdSet = new Set(coreStageIds);

    graphData.nodes.forEach((node) => {
        node.baseRadius = getNodeRadius(node.level);
        node.kindLabel = getKindLabel(node.level);
    });

    graphData.edges.forEach((edge) => {
        const sourceId = getEdgeSourceId(edge);
        const targetId = getEdgeTargetId(edge);

        if (edge.type === "parent-child" && childrenById.has(sourceId)) {
            childrenById.get(sourceId).push(targetId);
        }

        if (incomingById.has(targetId)) {
            incomingById.get(targetId).push(edge);
        }

        if (outgoingById.has(sourceId)) {
            outgoingById.get(sourceId).push(edge);
        }
    });

    childrenById.forEach((children) => {
        children.sort((leftId, rightId) => {
            const left = nodesById.get(leftId);
            const right = nodesById.get(rightId);
            return left.label.localeCompare(right.label, "zh-CN", { numeric: true });
        });
    });

    let width = window.innerWidth;
    let height = window.innerHeight;
    let currentTransform = d3.zoomIdentity;
    let viewMode = "home";
    let focusNodeId = null;
    let selectedId = null;
    let hoveredId = null;
    let visibleNodeIds = new Set();
    let currentVisibleEdges = [];
    let searchMatches = [];
    let activeSearchIndex = -1;
    let focusState = createEmptyFocusState();
    let layoutState = createDefaultLayoutState();
    const positionCache = new Map();

    const markerLayer = svg.append("defs");
    createMarker(markerLayer, "arrow-stage", "#94a3b8");
    createMarker(markerLayer, "arrow-bridge", "#fb923c");
    createMarker(markerLayer, "arrow-dependency", "#60a5fa");
    createMarker(markerLayer, "arrow-knowledge", "#34d399");

    const background = svg.append("rect").attr("class", "graph-background");
    const viewport = svg.append("g").attr("class", "viewport");
    const edgeLayer = viewport.append("g").attr("class", "edge-layer");
    const edgeLabelLayer = viewport.append("g").attr("class", "edge-label-layer");
    const nodeLayer = viewport.append("g").attr("class", "node-layer");

    const zoomBehavior = d3.zoom()
        .scaleExtent([0.55, 3.2])
        .on("zoom", (event) => {
            currentTransform = event.transform;
            viewport.attr("transform", currentTransform);
        });

    svg.call(zoomBehavior).on("dblclick.zoom", null);

    background.on("click", () => {
        tooltip.hidden = true;
        hoveredId = null;
        updateHighlightState();

        if (viewMode === "focus") {
            goHome();
            return;
        }

        selectedId = null;
        renderInfoPanel();
        updateSelectionClasses();
    });

    function renderGraph(animate = false) {
        const scene = viewMode === "home" ? buildHomeScene() : buildFocusScene();
        const visibleNodes = Array.from(scene.visibleNodeIds)
            .map((id) => nodesById.get(id))
            .filter(Boolean);

        visibleNodeIds = scene.visibleNodeIds;
        currentVisibleEdges = decorateParallelEdges(scene.edges);
        layoutState = scene.layout;

        visibleNodes.forEach((node) => {
            const target = scene.positions.get(node.id);
            node.x = target.x;
            node.y = target.y;
        });

        applyViewStateClasses();
        applyDynamicMetrics();

        const transitionDuration = animate ? 520 : 220;

        const edgeSelection = edgeLayer.selectAll("path.edge").data(currentVisibleEdges, (edge) => edge.id);

        edgeSelection.exit()
            .transition()
            .duration(180)
            .style("opacity", 0)
            .remove();

        const edgeEnter = edgeSelection.enter()
            .append("path")
            .attr("class", (edge) => buildEdgeClass(edge))
            .attr("fill", "none")
            .style("opacity", 0)
            .attr("marker-end", (edge) => getMarkerUrl(edge))
            .attr("stroke", (edge) => getEdgeStroke(edge))
            .attr("stroke-width", (edge) => getDefaultEdgeWidth(edge))
            .attr("d", (edge) => getEdgePath(edge));

        edgeEnter.merge(edgeSelection)
            .attr("class", (edge) => buildEdgeClass(edge))
            .attr("marker-end", (edge) => getMarkerUrl(edge))
            .attr("stroke", (edge) => getEdgeStroke(edge))
            .transition()
            .duration(transitionDuration)
            .style("opacity", 1)
            .attr("stroke-width", (edge) => getDefaultEdgeWidth(edge))
            .attr("d", (edge) => getEdgePath(edge));

        const edgeLabelSelection = edgeLabelLayer.selectAll("g.edge-label-group").data(currentVisibleEdges, (edge) => edge.id);

        edgeLabelSelection.exit()
            .transition()
            .duration(180)
            .style("opacity", 0)
            .remove();

        const edgeLabelEnter = edgeLabelSelection.enter()
            .append("g")
            .attr("class", (edge) => `edge-label-group edge-label-group-${getEdgeLabelTone(edge)}`)
            .style("opacity", 0);

        edgeLabelEnter.append("rect")
            .attr("class", "edge-label-bg")
            .attr("rx", 10)
            .attr("ry", 10);

        edgeLabelEnter.append("text")
            .attr("class", (edge) => `edge-label edge-label-${getEdgeLabelTone(edge)}`);

        const mergedEdgeLabels = edgeLabelEnter.merge(edgeLabelSelection)
            .attr("class", (edge) => `edge-label-group edge-label-group-${getEdgeLabelTone(edge)}`)
            .attr("transform", (edge) => getEdgeLabelTransform(edge));

        mergedEdgeLabels.select("text")
            .attr("class", (edge) => `edge-label edge-label-${getEdgeLabelTone(edge)}`)
            .each(function (edge) {
                renderMultilineText(d3.select(this), wrapLabel(getEdgeLabel(edge), getEdgeLabelCharLimit(edge), 2), getEdgeLabelLineHeight(), 0);
            });

        mergedEdgeLabels.transition()
            .duration(transitionDuration)
            .style("opacity", 1)
            .attr("transform", (edge) => getEdgeLabelTransform(edge));

        const nodeSelection = nodeLayer.selectAll("g.node").data(visibleNodes, (node) => node.id);

        nodeSelection.exit()
            .transition()
            .duration(220)
            .style("opacity", 0)
            .remove();

        const nodeEnter = nodeSelection.enter()
            .append("g")
            .attr("class", (node) => buildNodeClass(node))
            .style("opacity", 0)
            .attr("transform", (node) => {
                const origin = getNodeEnterPosition(node.id);
                return `translate(${origin.x}, ${origin.y})`;
            })
            .on("mouseenter", (event, node) => {
                hoveredId = node.id;
                updateHighlightState();
                tooltip.hidden = false;
                tooltip.innerHTML = buildTooltip(node);
                positionTooltip(event);
            })
            .on("mousemove", (event) => {
                positionTooltip(event);
            })
            .on("mouseleave", () => {
                hoveredId = null;
                updateHighlightState();
                tooltip.hidden = true;
            })
            .on("click", (event, node) => {
                event.stopPropagation();
                tooltip.hidden = true;

                if (viewMode === "focus" && node.id === focusNodeId) {
                    selectedId = node.id;
                    renderInfoPanel();
                    updateSelectionClasses();
                    return;
                }

                enterFocusView(node.id);
            });

        nodeEnter.append("circle").attr("class", "node-circle");

        nodeEnter.append("text")
            .attr("class", "node-label")
            .attr("data-role", "label");

        const badgeEnter = nodeEnter.append("g")
            .attr("class", "node-badge-group");

        badgeEnter.append("circle")
            .attr("class", "node-badge")
            .attr("r", 8);

        badgeEnter.append("text")
            .attr("class", "node-badge-text");

        const mergedNodes = nodeEnter.merge(nodeSelection)
            .attr("class", (node) => buildNodeClass(node));

        mergedNodes.select(".node-circle")
            .attr("fill", (node) => getNodeFill(node))
            .attr("stroke", (node) => getNodeStroke(node))
            .transition()
            .duration(transitionDuration)
            .attr("r", (node) => getDisplayNodeRadius(node))
            .attr("stroke-width", (node) => getNodeStrokeWidth(node))
            .attr("opacity", (node) => getNodeOpacity(node));

        mergedNodes.select(".node-label")
            .each(function (node) {
                const text = d3.select(this)
                    .attr("font-size", getNodeFontSize(node));

                renderMultilineText(text, wrapLabel(node.label, getNodeLabelCharLimit(node), 2), getNodeLineHeight(node), getDisplayNodeRadius(node) + 10);
            });

        mergedNodes.select(".node-badge-group")
            .style("display", (node) => shouldShowBadge(node) ? null : "none")
            .transition()
            .duration(transitionDuration)
            .attr("transform", (node) => `translate(${getDisplayNodeRadius(node) * 0.72}, ${-getDisplayNodeRadius(node) * 0.72})`);

        mergedNodes.select(".node-badge-text")
            .text((node) => node.childCount);

        mergedNodes.transition()
            .duration(transitionDuration)
            .style("opacity", 1)
            .attr("transform", (node) => `translate(${node.x}, ${node.y})`);

        refreshEdgeLabelBubbles();
        updateSelectionClasses();
        updateHighlightState();
        persistPositions(visibleNodes);
    }

    function buildHomeScene() {
        const frame = getGraphFrame();
        const visibleIds = new Set(coreStageIds);
        const positions = new Map();
        const count = coreStageIds.length;
        const spacing = count > 1 ? frame.width / Math.max(count - 1, 1) : 0;
        const centerY = frame.centerY;

        coreStageIds.forEach((id, index) => {
            positions.set(id, {
                x: frame.left + spacing * index,
                y: centerY
            });
        });

        return {
            visibleNodeIds: visibleIds,
            positions,
            edges: buildHomeEdges(),
            layout: {
                frame,
                baseRadius: clamp(frame.width / 18, 30, 56),
                nodeFontSize: clamp(frame.width / 70, 13, 18),
                edgeLabelFontSize: clamp(frame.width / 110, 9, 12),
                maxLayerSize: count,
                layerHeight: 0,
                nodeSpacing: spacing || frame.width,
                homeRadius: clamp(frame.width / 18, 30, 56)
            }
        };
    }

    function buildHomeEdges() {
        const edges = [];
        const aggregateMap = new Map();

        graphData.edges.forEach((edge) => {
            const sourceId = getEdgeSourceId(edge);
            const targetId = getEdgeTargetId(edge);

            if (edge.type === "stage-flow" && coreStageIdSet.has(sourceId) && coreStageIdSet.has(targetId)) {
                edges.push(createRenderableEdge({
                    id: `home:stage:${sourceId}->${targetId}`,
                    sourceId,
                    targetId,
                    type: "stage-flow",
                    label: "阶段推进"
                }));
                return;
            }

            if (edge.type === "parent-child" || edge.type === "stage-flow") {
                return;
            }

            const sourceNode = nodesById.get(sourceId);
            const targetNode = nodesById.get(targetId);
            if (!sourceNode || !targetNode) {
                return;
            }

            const sourceStageId = sourceNode.stageId;
            const targetStageId = targetNode.stageId;

            if (sourceStageId === targetStageId || !coreStageIdSet.has(sourceStageId) || !coreStageIdSet.has(targetStageId)) {
                return;
            }

            const key = `${edge.type}:${sourceStageId}->${targetStageId}`;
            if (!aggregateMap.has(key)) {
                aggregateMap.set(key, []);
            }
            aggregateMap.get(key).push(edge);
        });

        aggregateMap.forEach((items, key) => {
            const [type, pair] = key.split(":");
            const [sourceId, targetId] = pair.split("->");
            const sourceNode = nodesById.get(sourceId);
            const targetNode = nodesById.get(targetId);

            edges.push(createRenderableEdge({
                id: `home:${type}:${sourceId}->${targetId}`,
                sourceId,
                targetId,
                type,
                homeAggregate: true,
                label: formatHomeEdgeLabel(type, sourceNode, targetNode, items.length)
            }));
        });

        return edges;
    }

    function buildFocusScene() {
        const focusNode = nodesById.get(focusNodeId);
        if (!focusNode) {
            viewMode = "home";
            return buildHomeScene();
        }

        focusState = computeFocusState(focusNodeId);
        const frame = getGraphFrame();
        const layout = computeFocusLayout(frame, focusState);
        const positions = computeFocusPositions(frame, focusState, layout);

        return {
            visibleNodeIds: focusState.visibleIds,
            positions,
            edges: buildFocusEdges(focusState.visibleIds),
            layout
        };
    }

    function computeFocusState(nodeId) {
        const node = nodesById.get(nodeId);
        const ancestry = getAncestry(nodeId).slice(0, -1).reverse();
        const incomingCrossEdges = (incomingById.get(nodeId) || []).filter((edge) => edge.type !== "parent-child");
        const outgoingCrossEdges = (outgoingById.get(nodeId) || []).filter((edge) => edge.type !== "parent-child");
        const childIds = childrenById.get(nodeId) || [];
        const upstreamLayers = new Map();
        const downstreamLayers = new Map();
        const visibleIds = new Set([nodeId]);
        const primaryNodeIds = new Set();
        const secondaryNodeIds = new Set();
        const primaryParentEdgeIds = new Set();
        const upstreamPanelItems = [];
        const downstreamPanelItems = [];

        ancestry.forEach((ancestor, index) => {
            const depth = index + 1;
            addLayerItem(upstreamLayers, depth, {
                id: ancestor.id,
                primary: true,
                relationType: "parent-child",
                reason: depth === 1 ? "直接父级" : `上游第 ${depth} 层父级`
            });
            visibleIds.add(ancestor.id);
            primaryNodeIds.add(ancestor.id);
            upstreamPanelItems.push({
                id: ancestor.id,
                description: `上游母子关系 · ${ancestor.kindLabel} · ${depth === 1 ? "直接父级" : `上游第 ${depth} 层`}`,
                depth
            });
        });

        incomingCrossEdges.forEach((edge) => {
            const sourceId = getEdgeSourceId(edge);
            addLayerItem(upstreamLayers, 1, {
                id: sourceId,
                primary: false,
                relationType: edge.type,
                reason: edge.label || getFallbackEdgeLabel(edge)
            });
            visibleIds.add(sourceId);

            if (sourceId !== nodeId && !primaryNodeIds.has(sourceId)) {
                secondaryNodeIds.add(sourceId);
            }

            const sourceNode = nodesById.get(sourceId);
            if (sourceNode) {
                upstreamPanelItems.push({
                    id: sourceId,
                    description: `关联输入 · ${edge.label || getFallbackEdgeLabel(edge)}`,
                    depth: 1
                });
            }
        });

        childIds.forEach((childId) => {
            addLayerItem(downstreamLayers, 1, {
                id: childId,
                primary: true,
                relationType: "parent-child",
                reason: "直接子级"
            });
            visibleIds.add(childId);
            primaryNodeIds.add(childId);

            const childNode = nodesById.get(childId);
            if (childNode) {
                downstreamPanelItems.push({
                    id: childId,
                    description: `下游母子关系 · ${childNode.kindLabel} · ${childNode.childCount} 个直接子节点`,
                    depth: 1
                });
            }
        });

        outgoingCrossEdges.forEach((edge) => {
            const targetId = getEdgeTargetId(edge);
            addLayerItem(downstreamLayers, 1, {
                id: targetId,
                primary: false,
                relationType: edge.type,
                reason: edge.label || getFallbackEdgeLabel(edge)
            });
            visibleIds.add(targetId);

            if (targetId !== nodeId && !primaryNodeIds.has(targetId)) {
                secondaryNodeIds.add(targetId);
            }

            const targetNode = nodesById.get(targetId);
            if (targetNode) {
                downstreamPanelItems.push({
                    id: targetId,
                    description: `关联输出 · ${edge.label || getFallbackEdgeLabel(edge)}`,
                    depth: 1
                });
            }
        });

        upstreamLayers.forEach((items) => sortLayerItems(items));
        downstreamLayers.forEach((items) => sortLayerItems(items));

        graphData.edges.forEach((edge) => {
            const sourceId = getEdgeSourceId(edge);
            const targetId = getEdgeTargetId(edge);

            if (!visibleIds.has(sourceId) || !visibleIds.has(targetId)) {
                return;
            }

            if (edge.type === "parent-child") {
                primaryParentEdgeIds.add(buildEdgeId(edge.type, sourceId, targetId));
            }
        });

        return {
            focusNode: node,
            visibleIds,
            upstreamLayers,
            downstreamLayers,
            primaryNodeIds,
            secondaryNodeIds,
            primaryParentEdgeIds,
            upstreamPanelItems: dedupePanelItems(upstreamPanelItems),
            downstreamPanelItems: dedupePanelItems(downstreamPanelItems)
        };
    }

    function computeFocusLayout(frame, state) {
        const upstreamDepthCount = state.upstreamLayers.size;
        const downstreamDepthCount = state.downstreamLayers.size;
        const totalBands = upstreamDepthCount + 1 + downstreamDepthCount;
        const maxLayerSize = Math.max(
            1,
            ...Array.from(state.upstreamLayers.values()).map((items) => items.length),
            ...Array.from(state.downstreamLayers.values()).map((items) => items.length)
        );

        return {
            frame,
            baseRadius: clamp(Math.min(frame.width / Math.max(maxLayerSize * 6, 6), frame.height / Math.max(totalBands * 5, 5)), 10, 24),
            nodeFontSize: clamp(frame.width / Math.max(maxLayerSize * 13, 13), 9, 14),
            edgeLabelFontSize: clamp(frame.width / Math.max(maxLayerSize * 18, 18), 8, 11),
            layerHeight: clamp(frame.height / Math.max(totalBands + 0.8, 2), 84, 148),
            nodeSpacing: clamp(frame.width / Math.max(maxLayerSize + 0.8, 2), 72, 180),
            homeRadius: clamp(frame.width / 18, 30, 56),
            maxLayerSize
        };
    }

    function computeFocusPositions(frame, state, layout) {
        const positions = new Map();
        const centerX = frame.centerX;
        const centerY = frame.centerY;

        positions.set(state.focusNode.id, { x: centerX, y: centerY });

        state.upstreamLayers.forEach((items, depth) => {
            assignLayerPositions(items, depth, "upstream", positions, frame, layout, centerX, centerY);
        });

        state.downstreamLayers.forEach((items, depth) => {
            assignLayerPositions(items, depth, "downstream", positions, frame, layout, centerX, centerY);
        });

        return positions;
    }

    function assignLayerPositions(items, depth, direction, positions, frame, layout, centerX, centerY) {
        const y = direction === "upstream"
            ? centerY - depth * layout.layerHeight
            : centerY + depth * layout.layerHeight;
        const usableWidth = Math.max(frame.width - layout.baseRadius * 2, layout.nodeSpacing);
        const layerSpacing = items.length <= 1
            ? 0
            : Math.min(layout.nodeSpacing, usableWidth / Math.max(items.length - 1, 1));
        const totalWidth = layerSpacing * Math.max(items.length - 1, 0);

        items.forEach((item, index) => {
            positions.set(item.id, {
                x: centerX - totalWidth / 2 + index * layerSpacing,
                y
            });
        });
    }

    function buildFocusEdges(visibleIds) {
        return graphData.edges
            .filter((edge) => visibleIds.has(getEdgeSourceId(edge)) && visibleIds.has(getEdgeTargetId(edge)))
            .map((edge) => createRenderableEdge(edge));
    }

    function createRenderableEdge(edge) {
        const sourceId = edge.sourceId || getEdgeSourceId(edge);
        const targetId = edge.targetId || getEdgeTargetId(edge);

        return {
            ...edge,
            id: edge.id || buildEdgeId(edge.type, sourceId, targetId),
            sourceId,
            targetId,
            label: edge.label || getFallbackEdgeLabel(edge)
        };
    }

    function decorateParallelEdges(edges) {
        const grouped = new Map();

        edges.forEach((edge) => {
            const key = `${edge.sourceId}->${edge.targetId}`;
            if (!grouped.has(key)) {
                grouped.set(key, []);
            }
            grouped.get(key).push(edge);
        });

        grouped.forEach((group) => {
            group
                .sort((left, right) => getEdgeTypeOrder(left.type) - getEdgeTypeOrder(right.type))
                .forEach((edge, index) => {
                    edge.parallelIndex = index;
                    edge.parallelCount = group.length;
                });
        });

        return edges;
    }

    function updateSelectionClasses() {
        nodeLayer.selectAll("g.node")
            .classed("is-selected", (node) => node.id === selectedId)
            .classed("is-focus-target", (node) => viewMode === "focus" && node.id === focusNodeId)
            .classed("is-parent-child-related", (node) => viewMode === "focus" && focusState.primaryNodeIds.has(node.id))
            .classed("is-secondary-related", (node) => viewMode === "focus" && focusState.secondaryNodeIds.has(node.id));

        edgeLayer.selectAll("path.edge")
            .classed("is-primary-parent", (edge) => viewMode === "focus" && focusState.primaryParentEdgeIds.has(edge.id));
    }

    function updateHighlightState() {
        const highlightedNodes = new Set();
        const highlightedEdges = new Set();

        if (hoveredId) {
            highlightedNodes.add(hoveredId);

            currentVisibleEdges.forEach((edge) => {
                if (edge.sourceId === hoveredId || edge.targetId === hoveredId) {
                    highlightedNodes.add(edge.sourceId);
                    highlightedNodes.add(edge.targetId);
                    highlightedEdges.add(edge.id);
                }
            });
        }

        nodeLayer.selectAll("g.node")
            .classed("is-highlighted", (node) => hoveredId && highlightedNodes.has(node.id))
            .classed("is-dimmed", (node) => hoveredId && !highlightedNodes.has(node.id));

        edgeLayer.selectAll("path.edge")
            .classed("is-highlighted", (edge) => hoveredId && highlightedEdges.has(edge.id))
            .classed("is-dimmed", (edge) => hoveredId && !highlightedEdges.has(edge.id))
            .attr("stroke-width", (edge) => hoveredId && highlightedEdges.has(edge.id)
                ? getHighlightedEdgeWidth(edge)
                : getDefaultEdgeWidth(edge));

        edgeLabelLayer.selectAll("g.edge-label-group")
            .classed("is-dimmed", (edge) => hoveredId && !highlightedEdges.has(edge.id));
    }

    function refreshEdgeLabelBubbles() {
        edgeLabelLayer.selectAll("g.edge-label-group").each(function () {
            const group = d3.select(this);
            const text = group.select("text");
            const rect = group.select("rect");
            const box = text.node().getBBox();
            const horizontalPadding = 8;
            const verticalPadding = 5;

            rect
                .attr("x", box.x - horizontalPadding)
                .attr("y", box.y - verticalPadding)
                .attr("width", box.width + horizontalPadding * 2)
                .attr("height", box.height + verticalPadding * 2);
        });
    }

    function enterFocusView(nodeId) {
        const node = nodesById.get(nodeId);
        if (!node) {
            return;
        }

        viewMode = "focus";
        focusNodeId = nodeId;
        selectedId = nodeId;
        renderGraph(true);
        renderInfoPanel();
        resetView();
    }

    function goHome() {
        viewMode = "home";
        focusNodeId = null;
        selectedId = null;
        focusState = createEmptyFocusState();
        renderGraph(true);
        renderInfoPanel();
        resetView();
    }

    function renderInfoPanel() {
        infoPanel.style.display = "";

        if (viewMode === "home") {
            infoPanel.innerHTML = `
                ${getInfoPanelCloseButton()}
                <h2 class="info-title">人工智能知识图谱</h2>
                <p class="info-subtitle">首页只保留四大核心模块与它们之间的直接关系。单击任意节点进入聚焦视图，聚焦对象居中，上游在上层水平平铺，下游在下层水平平铺。</p>
                <div class="info-badges">
                    <span class="info-badge">4 个核心模块</span>
                    <span class="info-badge">${graphData.meta.moduleCount} 个主题模块</span>
                    <span class="info-badge">${graphData.meta.knowledgePointCount} 个知识点</span>
                    <span class="info-badge">搜索可直达任意节点</span>
                </div>
                <div class="info-section">
                    <div class="info-section-title">浏览方式</div>
                    <div class="info-empty">首页只展示核心模块的阶段推进与跨模块依赖。点击节点后，会同时展示它的上下游母子关系以及直接关联关系，并为所有可见连线附上关系说明。</div>
                </div>
            `;
            bindInfoPanelInteractions();
            return;
        }

        const focusNode = nodesById.get(focusNodeId);
        if (!focusNode) {
            return;
        }

        const breadcrumbNodes = getAncestry(focusNode.id);
        const upstreamMarkup = focusState.upstreamPanelItems.length > 0
            ? focusState.upstreamPanelItems
                .sort((left, right) => left.depth - right.depth || nodesById.get(left.id).label.localeCompare(nodesById.get(right.id).label, "zh-CN", { numeric: true }))
                .map((item) => createActionButton(item.id, nodesById.get(item.id).label, item.description))
                .join("")
            : '<div class="info-empty">当前节点没有显式的上游关系。</div>';
        const downstreamMarkup = focusState.downstreamPanelItems.length > 0
            ? focusState.downstreamPanelItems
                .sort((left, right) => left.depth - right.depth || nodesById.get(left.id).label.localeCompare(nodesById.get(right.id).label, "zh-CN", { numeric: true }))
                .map((item) => createActionButton(item.id, nodesById.get(item.id).label, item.description))
                .join("")
            : '<div class="info-empty">当前节点没有显式的下游关系。</div>';

        infoPanel.innerHTML = `
            ${getInfoPanelCloseButton()}
            <h2 class="info-title">${escapeHtml(focusNode.label)}</h2>
            <p class="info-subtitle">${escapeHtml(focusNode.fullPath)}</p>
            <div class="info-badges">
                <span class="info-badge">${escapeHtml(focusNode.kindLabel)}</span>
                <span class="info-badge">${escapeHtml(nodesById.get(focusNode.stageId).label)}</span>
                <span class="info-badge">上游 ${focusState.upstreamPanelItems.length}</span>
                <span class="info-badge">下游 ${focusState.downstreamPanelItems.length}</span>
            </div>
            <div class="info-section">
                <div class="info-section-title">面包屑路径</div>
                <div class="info-breadcrumbs">
                    ${breadcrumbNodes.map((item) => createActionButton(item.id, item.label, item.kindLabel)).join("")}
                </div>
            </div>
            <div class="info-section">
                <div class="info-section-title">上游关系</div>
                <div class="info-list">${upstreamMarkup}</div>
            </div>
            <div class="info-section">
                <div class="info-section-title">下游关系</div>
                <div class="info-list">${downstreamMarkup}</div>
            </div>
        `;

        bindInfoPanelInteractions();
    }

    function bindInfoPanelInteractions() {
        const closeButton = infoPanel.querySelector(".info-close");
        if (closeButton) {
            closeButton.addEventListener("click", () => {
                infoPanel.style.display = "none";
            });
        }

        infoPanel.querySelectorAll("[data-node-id]").forEach((element) => {
            element.addEventListener("click", (event) => {
                const nodeId = event.currentTarget.getAttribute("data-node-id");
                enterFocusView(nodeId);
            });
        });
    }

    function bindSearchEvents() {
        searchInput.addEventListener("input", () => {
            const keyword = searchInput.value.trim();
            activeSearchIndex = -1;

            if (!keyword) {
                searchMatches = [];
                renderSearchResults();
                return;
            }

            const normalizedKeyword = normalizeText(keyword);
            searchMatches = graphData.nodes
                .filter((node) => {
                    const haystack = [node.label, node.rawName, node.fullPath, node.breadcrumb].join(" ");
                    return normalizeText(haystack).includes(normalizedKeyword);
                })
                .sort((left, right) => {
                    if (left.level !== right.level) {
                        return left.level - right.level;
                    }
                    return left.fullPath.localeCompare(right.fullPath, "zh-CN", { numeric: true });
                })
                .slice(0, 12);

            renderSearchResults();
        });

        searchInput.addEventListener("keydown", (event) => {
            if (searchMatches.length === 0) {
                if (event.key === "Escape") {
                    searchMatches = [];
                    activeSearchIndex = -1;
                    renderSearchResults();
                }
                return;
            }

            if (event.key === "ArrowDown") {
                event.preventDefault();
                activeSearchIndex = (activeSearchIndex + 1) % searchMatches.length;
                renderSearchResults();
            }

            if (event.key === "ArrowUp") {
                event.preventDefault();
                activeSearchIndex = activeSearchIndex <= 0 ? searchMatches.length - 1 : activeSearchIndex - 1;
                renderSearchResults();
            }

            if (event.key === "Enter") {
                event.preventDefault();
                const target = searchMatches[Math.max(activeSearchIndex, 0)];
                if (target) {
                    activateSearchResult(target.id);
                }
            }

            if (event.key === "Escape") {
                searchMatches = [];
                activeSearchIndex = -1;
                renderSearchResults();
            }
        });
    }

    function renderSearchResults() {
        if (searchMatches.length === 0) {
            if (searchInput.value.trim()) {
                searchResults.hidden = false;
                searchResults.innerHTML = '<div class="search-empty">没有找到匹配项，可以尝试更短的关键词。</div>';
            } else {
                searchResults.hidden = true;
                searchResults.innerHTML = "";
            }
            return;
        }

        searchResults.hidden = false;
        searchResults.innerHTML = searchMatches.map((node, index) => `
            <div class="search-item ${index === activeSearchIndex ? "is-active" : ""}" data-node-id="${escapeHtml(node.id)}">
                <div class="search-item-title">${escapeHtml(node.label)}</div>
                <div class="search-item-meta">${escapeHtml(node.kindLabel)} · ${escapeHtml(node.breadcrumb)}</div>
            </div>
        `).join("");

        searchResults.querySelectorAll(".search-item").forEach((element) => {
            element.addEventListener("click", () => {
                activateSearchResult(element.getAttribute("data-node-id"));
            });
        });
    }

    function activateSearchResult(nodeId) {
        searchMatches = [];
        activeSearchIndex = -1;
        renderSearchResults();
        enterFocusView(nodeId);
        searchInput.blur();
    }

    function bindToolbarEvents() {
        resetViewButton.addEventListener("click", () => {
            if (viewMode === "focus") {
                goHome();
                return;
            }

            selectedId = null;
            renderInfoPanel();
            resetView();
        });
    }

    function bindKeyboardShortcuts() {
        window.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && viewMode === "focus") {
                goHome();
            }
        });
    }

    function handleResize() {
        width = window.innerWidth;
        height = window.innerHeight;
        svg.attr("viewBox", [0, 0, width, height].join(" "));
        background.attr("width", width).attr("height", height);
        renderGraph(false);
        renderInfoPanel();
    }

    function resetView() {
        svg.transition().duration(520).call(zoomBehavior.transform, d3.zoomIdentity);
    }

    function buildNodeClass(node) {
        return `node node-level-${node.level}`;
    }

    function buildEdgeClass(edge) {
        const extraClass = edge.type === "parent-child" && viewMode === "focus" && focusState.primaryParentEdgeIds.has(edge.id)
            ? " is-primary-parent"
            : "";
        return `edge edge-${edge.type}${extraClass}`;
    }

    function getNodeEnterPosition(nodeId) {
        if (positionCache.has(nodeId)) {
            return positionCache.get(nodeId);
        }

        if (focusNodeId && positionCache.has(focusNodeId)) {
            return positionCache.get(focusNodeId);
        }

        const frame = layoutState.frame || getGraphFrame();
        return { x: frame.centerX, y: frame.centerY };
    }

    function persistPositions(nodes) {
        nodes.forEach((node) => {
            positionCache.set(node.id, { x: node.x, y: node.y });
        });
    }

    function getGraphFrame() {
        const compact = width < 1180;
        const leftInset = compact ? 40 : 260;
        const rightInset = compact ? 40 : 420;
        const topInset = compact ? 170 : 84;
        const bottomInset = compact ? 110 : 92;
        const left = leftInset;
        const right = Math.max(width - rightInset, left + 240);
        const top = topInset;
        const bottom = Math.max(height - bottomInset, top + 260);

        return {
            left,
            right,
            top,
            bottom,
            width: right - left,
            height: bottom - top,
            centerX: left + (right - left) / 2,
            centerY: top + (bottom - top) / 2
        };
    }

    function applyViewStateClasses() {
        svg.classed("view-home", viewMode === "home");
        svg.classed("view-focus", viewMode === "focus");
    }

    function applyDynamicMetrics() {
        document.documentElement.style.setProperty("--node-font-size", `${layoutState.nodeFontSize}px`);
        document.documentElement.style.setProperty("--edge-label-font-size", `${layoutState.edgeLabelFontSize}px`);
    }

    function getNodeFill(node) {
        return getStagePalette(node.stageId).fill;
    }

    function getNodeStroke(node) {
        return getStagePalette(node.stageId).stroke;
    }

    function getStagePalette(stageId) {
        return stageColors[stageId] || stageColors["02"];
    }

    function getDisplayNodeRadius(node) {
        if (viewMode === "home") {
            return layoutState.homeRadius;
        }

        const role = getNodeRole(node.id);
        const base = layoutState.baseRadius * ([1.15, 1, 0.94, 0.88][node.level] || 1);

        if (role === "focus-target") {
            return base * 1.55;
        }

        if (role === "primary") {
            return base * 1.14;
        }

        return base;
    }

    function getNodeStrokeWidth(node) {
        if (viewMode === "home") {
            return 2.8;
        }

        const role = getNodeRole(node.id);
        if (role === "focus-target") {
            return 3.2;
        }

        if (role === "primary") {
            return 2.2;
        }

        return 1.6;
    }

    function getNodeOpacity(node) {
        if (viewMode === "home") {
            return 1;
        }

        return getNodeRole(node.id) === "secondary" ? 0.9 : 1;
    }

    function getNodeFontSize(node) {
        if (viewMode === "home") {
            return layoutState.nodeFontSize;
        }

        if (node.id === focusNodeId) {
            return Math.min(layoutState.nodeFontSize + 1, 15);
        }

        return layoutState.nodeFontSize;
    }

    function getNodeLineHeight(node) {
        return getNodeFontSize(node) * 1.08;
    }

    function getNodeLabelCharLimit(node) {
        if (viewMode === "home") {
            return 6;
        }

        if (node.id === focusNodeId) {
            return clamp(Math.round(layoutState.nodeSpacing / 18), 5, 10);
        }

        return clamp(Math.round(layoutState.nodeSpacing / 22), 4, 8);
    }

    function getEdgeLabelCharLimit(edge) {
        if (viewMode === "home") {
            return edge.type === "stage-flow" ? 6 : 10;
        }

        return clamp(Math.round(layoutState.nodeSpacing / 14), 7, 16);
    }

    function getEdgeLabelLineHeight() {
        return layoutState.edgeLabelFontSize * 1.04;
    }

    function shouldShowBadge(node) {
        if (viewMode === "home") {
            return node.childCount > 0;
        }

        return node.childCount > 0 && getNodeRole(node.id) !== "secondary";
    }

    function getNodeRole(nodeId) {
        if (viewMode !== "focus" || !focusNodeId) {
            return "home";
        }

        if (nodeId === focusNodeId) {
            return "focus-target";
        }

        if (focusState.primaryNodeIds.has(nodeId)) {
            return "primary";
        }

        if (focusState.secondaryNodeIds.has(nodeId)) {
            return "secondary";
        }

        return "other";
    }

    function getEdgePath(edge) {
        const source = nodesById.get(edge.sourceId);
        const target = nodesById.get(edge.targetId);

        if (!source || !target) {
            return "";
        }

        const sourceX = source.x;
        const sourceY = source.y;
        const targetX = target.x;
        const targetY = target.y;

        if (edge.type === "parent-child") {
            return `M${sourceX},${sourceY}L${targetX},${targetY}`;
        }

        const dx = targetX - sourceX;
        const dy = targetY - sourceY;
        const distance = Math.sqrt(dx * dx + dy * dy) || 1;
        const midX = (sourceX + targetX) / 2;
        const midY = (sourceY + targetY) / 2;
        const parallelOffset = ((edge.parallelIndex || 0) - ((edge.parallelCount || 1) - 1) / 2) * 28;
        const curveOffset = Math.min(distance * 0.12, 48) + parallelOffset;
        const normalX = (-dy / distance) * curveOffset;
        const normalY = (dx / distance) * curveOffset;

        return `M${sourceX},${sourceY}Q${midX + normalX},${midY + normalY},${targetX},${targetY}`;
    }

    function getEdgeLabelTransform(edge) {
        const source = nodesById.get(edge.sourceId);
        const target = nodesById.get(edge.targetId);

        if (!source || !target) {
            return "translate(0, 0)";
        }

        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;

        if (edge.type === "parent-child") {
            return `translate(${midX + 18}, ${midY})`;
        }

        const dx = target.x - source.x;
        const dy = target.y - source.y;
        const distance = Math.sqrt(dx * dx + dy * dy) || 1;
        const parallelOffset = ((edge.parallelIndex || 0) - ((edge.parallelCount || 1) - 1) / 2) * 28;
        const curveOffset = Math.min(distance * 0.12, 48) + parallelOffset;
        const normalX = (-dy / distance) * curveOffset * 0.72;
        const normalY = (dx / distance) * curveOffset * 0.72;

        return `translate(${midX + normalX}, ${midY + normalY})`;
    }

    function getEdgeStroke(edge) {
        if (edge.type === "stage-flow") {
            return "#94a3b8";
        }

        if (edge.type === "bridge") {
            return "#fb923c";
        }

        if (edge.type === "dependency") {
            return "#60a5fa";
        }

        if (edge.type === "knowledge-link") {
            return "#34d399";
        }

        const sourceNode = nodesById.get(edge.sourceId);
        return sourceNode ? getStagePalette(sourceNode.stageId).stroke : "rgba(255,255,255,0.48)";
    }

    function getDefaultEdgeWidth(edge) {
        if (edge.type === "stage-flow") {
            return viewMode === "home" ? 3.4 : 3;
        }

        if (edge.type === "parent-child") {
            return focusState.primaryParentEdgeIds.has(edge.id) ? 2.8 : 1.8;
        }

        if (edge.type === "bridge") {
            return 2.1;
        }

        if (edge.type === "dependency") {
            return edge.homeAggregate ? 2.6 : 2.2;
        }

        return edge.homeAggregate ? 2.3 : 1.9;
    }

    function getHighlightedEdgeWidth(edge) {
        return getDefaultEdgeWidth(edge) + 0.9;
    }

    function getEdgeLabelTone(edge) {
        if (edge.type === "stage-flow") {
            return "stage";
        }

        if (edge.type === "parent-child") {
            return "child";
        }

        if (edge.type === "knowledge-link") {
            return "knowledge";
        }

        if (edge.type === "dependency") {
            return "dependency";
        }

        return "bridge";
    }

    function getMarkerUrl(edge) {
        if (edge.type === "stage-flow") {
            return "url(#arrow-stage)";
        }

        if (edge.type === "bridge") {
            return "url(#arrow-bridge)";
        }

        if (edge.type === "dependency") {
            return "url(#arrow-dependency)";
        }

        if (edge.type === "knowledge-link") {
            return "url(#arrow-knowledge)";
        }

        return null;
    }

    function formatHomeEdgeLabel(type, sourceNode, targetNode, count) {
        if (type === "dependency") {
            return `${sourceNode.label}支撑${targetNode.label}${count > 1 ? ` · ${count} 条` : ""}`;
        }

        if (type === "knowledge-link") {
            return `${sourceNode.label}衔接${targetNode.label}${count > 1 ? ` · ${count} 条` : ""}`;
        }

        return `${sourceNode.label}桥接${targetNode.label}${count > 1 ? ` · ${count} 条` : ""}`;
    }

    function addLayerItem(layerMap, depth, item) {
        if (!layerMap.has(depth)) {
            layerMap.set(depth, []);
        }

        const bucket = layerMap.get(depth);
        const existing = bucket.find((candidate) => candidate.id === item.id);

        if (existing) {
            existing.primary = existing.primary || item.primary;
            if (!existing.reason && item.reason) {
                existing.reason = item.reason;
            }
            return;
        }

        bucket.push(item);
    }

    function sortLayerItems(items) {
        const primary = items
            .filter((item) => item.primary)
            .sort((left, right) => nodesById.get(left.id).label.localeCompare(nodesById.get(right.id).label, "zh-CN", { numeric: true }));
        const secondary = items
            .filter((item) => !item.primary)
            .sort((left, right) => nodesById.get(left.id).label.localeCompare(nodesById.get(right.id).label, "zh-CN", { numeric: true }));
        const leftSecondary = secondary.slice(0, Math.floor(secondary.length / 2));
        const rightSecondary = secondary.slice(Math.floor(secondary.length / 2));

        items.length = 0;
        items.push(...leftSecondary, ...primary, ...rightSecondary);
    }

    function dedupePanelItems(items) {
        const seen = new Set();
        return items.filter((item) => {
            const key = `${item.id}:${item.description}`;
            if (seen.has(key)) {
                return false;
            }
            seen.add(key);
            return true;
        });
    }

    function getAncestry(nodeId) {
        const ancestry = [];
        let current = nodesById.get(nodeId);

        while (current) {
            ancestry.unshift(current);
            current = current.parentId ? nodesById.get(current.parentId) : null;
        }

        return ancestry;
    }

    function buildTooltip(node) {
        const actionHint = viewMode === "home"
            ? "单击进入该节点的聚焦视图"
            : node.id === focusNodeId
                ? "点击空白区域或按 Esc 返回首页"
                : "单击切换为该节点聚焦";

        return `
            <strong>${escapeHtml(node.label)}</strong><br>
            <span style="color:var(--text-muted)">${escapeHtml(node.kindLabel)} · ${escapeHtml(nodesById.get(node.stageId).label)}</span>
            ${node.childCount > 0 ? `<br><span style="color:var(--text-muted)">直接子节点 ${node.childCount}</span>` : ""}
            <br><span style="color:var(--text-muted)">${escapeHtml(actionHint)}</span>
        `;
    }

    function positionTooltip(event) {
        const offset = 14;
        const tooltipWidth = tooltip.offsetWidth || 260;
        const tooltipHeight = tooltip.offsetHeight || 88;
        let left = event.clientX + offset;
        let top = event.clientY + offset;

        if (left + tooltipWidth > window.innerWidth - 12) {
            left = event.clientX - tooltipWidth - offset;
        }

        if (top + tooltipHeight > window.innerHeight - 12) {
            top = event.clientY - tooltipHeight - offset;
        }

        tooltip.style.left = `${Math.max(12, left)}px`;
        tooltip.style.top = `${Math.max(12, top)}px`;
    }

    function renderMultilineText(textSelection, lines, lineHeight, firstLineDy) {
        textSelection.text(null);
        lines.forEach((line, index) => {
            textSelection.append("tspan")
                .attr("x", 0)
                .attr("dy", index === 0 ? firstLineDy : lineHeight)
                .text(line);
        });
    }

    function wrapLabel(value, maxCharsPerLine, maxLines = 2) {
        const text = String(value || "").trim();
        if (!text) {
            return [""];
        }

        const chars = Array.from(text);
        const charLimit = Math.max(Number(maxCharsPerLine) || 1, 1);
        const lines = [];
        let index = 0;

        while (index < chars.length && lines.length < maxLines) {
            if (lines.length === maxLines - 1) {
                const tail = chars.slice(index);
                if (tail.length > charLimit) {
                    lines.push(`${tail.slice(0, Math.max(charLimit - 1, 1)).join("")}…`);
                } else {
                    lines.push(tail.join(""));
                }
                break;
            }

            lines.push(chars.slice(index, index + charLimit).join(""));
            index += charLimit;
        }

        return lines;
    }

    function createMarker(defs, id, color) {
        defs.append("marker")
            .attr("id", id)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 10)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", color);
    }

    function createEmptyFocusState() {
        return {
            visibleIds: new Set(),
            upstreamLayers: new Map(),
            downstreamLayers: new Map(),
            primaryNodeIds: new Set(),
            secondaryNodeIds: new Set(),
            primaryParentEdgeIds: new Set(),
            upstreamPanelItems: [],
            downstreamPanelItems: []
        };
    }

    function createDefaultLayoutState() {
        const frame = {
            left: 0,
            right: width,
            top: 0,
            bottom: height,
            width,
            height,
            centerX: width / 2,
            centerY: height / 2
        };

        return {
            frame,
            baseRadius: 20,
            nodeFontSize: 12,
            edgeLabelFontSize: 10,
            layerHeight: 120,
            nodeSpacing: 120,
            homeRadius: 42,
            maxLayerSize: 1
        };
    }

    function getNodeRadius(level) {
        return [40, 28, 16, 10][level] || 10;
    }

    function getKindLabel(level) {
        return ["阶段", "主题模块", "主题", "知识点"][level] || "节点";
    }

    function getEdgeTypeOrder(type) {
        return {
            "stage-flow": 0,
            "parent-child": 1,
            bridge: 2,
            dependency: 3,
            "knowledge-link": 4
        }[type] ?? 99;
    }

    function getFallbackEdgeLabel(edge) {
        if (edge.type === "parent-child") {
            return "包含";
        }

        if (edge.type === "stage-flow") {
            return "阶段推进";
        }

        if (edge.type === "bridge") {
            return "桥接关系";
        }

        if (edge.type === "dependency") {
            return "跨模块依赖";
        }

        return "知识衔接";
    }

    function getEdgeLabel(edge) {
        return edge.label || getFallbackEdgeLabel(edge);
    }

    function buildEdgeId(type, sourceId, targetId) {
        return `${type}:${sourceId}->${targetId}`;
    }

    function normalizeText(value) {
        return value.replace(/[_\s/]/g, "").toLowerCase();
    }

    function createActionButton(nodeId, title, description) {
        return `
            <button class="info-action" type="button" data-node-id="${escapeHtml(nodeId)}">
                <span>${escapeHtml(title)}</span>
                <small>${escapeHtml(description)}</small>
            </button>
        `;
    }

    function getInfoPanelCloseButton() {
        return '<button class="info-close" type="button" aria-label="关闭面板">&times;</button>';
    }

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function getEdgeSourceId(edge) {
        if (edge.sourceId) {
            return edge.sourceId;
        }

        return typeof edge.source === "object" ? edge.source.id : edge.source;
    }

    function getEdgeTargetId(edge) {
        if (edge.targetId) {
            return edge.targetId;
        }

        return typeof edge.target === "object" ? edge.target.id : edge.target;
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    bindSearchEvents();
    bindToolbarEvents();
    bindKeyboardShortcuts();
    handleResize();
    renderGraph(false);
    renderInfoPanel();
    window.addEventListener("resize", handleResize);
});
