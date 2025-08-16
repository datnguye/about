function initDiagram() {
    // Create mock Neo4j data structure for CONTEXT Engineering
    const config = {
        containerId: "context-engineering-diagram",
        visConfig: {
            nodes: {
                Person: {
                    color: "#312b2bff",
                    borderColor: "#ffffff",
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                },
                Data: {
                    color: "#F59E0B",
                    borderColor: "#ffffff", 
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                },
                CONTEXT: {
                    color: "#10B981",
                    borderColor: "#ffffff",
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                },
                Augmentation: {
                    color: "#1d27ef",
                    borderColor: "#ffffff",
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                },
                Function: {
                    color: "#EF4444",
                    borderColor: "#ffffff",
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                },
                Storage: {
                    color: "#8B5CF6",
                    borderColor: "#ffffff",
                    borderWidth: 3,
                    font: {
                        color: "#ffffff",
                        size: 14,
                        face: "Inter"
                    }
                }
            },
            edges: {
                PROVIDES: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                FEEDS_INTO: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                ACTIVATES: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                QUERIES: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                EXECUTES: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                GENERATES: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                RESPONDS_TO: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                ACCESSES: {
                    color: "#666666",
                    width: 1,
                    arrows: "to",
                    dashes: [5, 5],
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                STORES_IN: {
                    color: "#cccccc",
                    width: 2,
                    arrows: "to",
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                RETRIEVES_FROM: {
                    color: "#666666",
                    width: 1,
                    arrows: "to",
                    dashes: [5, 5],
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                },
                UPDATES: {
                    color: "#666666",
                    width: 1,
                    arrows: "to",
                    dashes: [5, 5],
                    font: {
                        color: "#aaaaaa",
                        size: 11,
                        face: "Inter",
                        background: "#1a1a1a",
                        strokeColor: "#444444",
                        strokeWidth: 1
                    }
                }
            },
            layout: {
                hierarchical: {
                    enabled: false
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 300,
                zoomView: true,
                dragView: true,
                dragNodes: true
            },
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 100
                },
                barnesHut: {
                    gravitationalConstant: -8000,
                    centralGravity: 0.3,
                    springLength: 120,
                    springConstant: 0.04,
                    damping: 0.09
                }
            }
        },
        initialCypher: "" // We'll use static data instead
    };

    // Create static graph data in Neo4j format with optimized positioning
    const graphData = {
        nodes: [
            {
                id: 1,
                label: " \uf007 User ",
                group: "Person",
                title: "The person interacting with the system",
                x: -200, y: 300
            },
            {
                id: 2,
                label: ' \uf075 Intent ',
                group: "Data", 
                title: "User input (questions, commands, queries)",
                x: -50, y: 300,
            },
            {
                id: 3,
                label: ' \uf0e8 Prompt ',
                group: "CONTEXT",
                title: "Aggregates input, memory, and schemas for the agent",
                x: 150, y: 300,
            },
            {
                id: 4,
                label: ' \uf544 Agent ',
                group: "Function",
                title: "Reasoning engine for decision making and orchestration",
                x: 400, y: 300,
            },
            {
                id: 5,
                label: ' \uf002 R-A-G ',
                group: "Augmentation",
                title: "Retrieval-Augmented Generation with vector search and/or knowlegde graph traversal",
                x: 650, y: 200,
            },
            {
                id: 6,
                label: ' \uf0ad Action Tools ',
                group: "Function",
                title: "APIs, SQL, code execution, external connectors",
                x: 650, y: 400,
            },
            {
                id: 7,
                label: '  \uf4ad Answer  ',
                group: "Data",
                title: "Final response delivered to the user",
                x: -50, y: 100,
            },
            {
                id: 8,
                label: ' \uf1c0 Long-Term\nMemory ',
                group: "Storage",
                title: "Persistent memory: MCP Servers + Databases",
                x: 400, y: 50,
            },
            {
                id: 9,
                label: ' \uf017 Short-Term\nMemory ',
                group: "Storage",
                title: "Session memory: stores recent chat history",
                x: 150, y: 500,
            }
        ],
        edges: [
            {
                from: 1, to: 2, label: "PROVIDES", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 2, to: 3, label: "FEEDS INTO", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 3, to: 4, label: "ACTIVATES", title: "", 
                color: { color: "#cccccc" }, width: 2, length: 250
            },
            {
                from: 4, to: 5, label: "QUERIES", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 4, to: 6, label: "EXECUTES", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 4, to: 7, label: "GENERATES", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 7, to: 1, label: "RESPONDS TO", title: "",
                color: { color: "#cccccc" }, width: 2
            },
            {
                from: 3, to: 9, label: "ACCESSES", title: "",
                color: { color: "#666666" }, width: 1, dashes: [5, 5]
            },
            {
                from: 7, to: 8, label: "STORES IN", title: "",
                color: { color: "#cccccc" }, width: 2, length: 250
            },
            {
                from: 5, to: 8, label: "RETRIEVES FROM", title: "",
                color: { color: "#666666" }, width: 1, dashes: [5, 5]
            },
            {
                from: 4, to: 3, label: "UPDATES", title: "",
                color: { color: "#666666" }, width: 1, dashes: [5, 5], length: 250
            }
        ]
    };
    
    // Use vis.js (Neo4j visualization library) to render the network
    renderNetwork();

    function renderNetwork() {
        const container = document.getElementById('context-engineering-diagram');
        
        // Make container relatively positioned to contain absolute positioned elements
        container.style.position = 'relative';
        
        const options = {
            nodes: {
                shape: 'circle',
                font: {
                    size: 35,
                    color: '#ffffff',
                    face: 'FontAwesome, Inter',
                    align: 'center',
                    multi: true,
                    vadjust: 0
                },
                borderWidth: 3,
                borderColor: '#201818ff',
                chosen: {
                    node: function(values, id, selected, hovering) {
                        values.borderWidth = 4;
                    }
                }
            },
            edges: {
                arrows: {
                    to: { enabled: true, scaleFactor: 0.5 }
                },
                font: {
                    size: 30,
                    color: '#aaaaaa',
                    face: 'Inter',
                    background: '#1a1a1a',
                    strokeColor: '#444444',
                    strokeWidth: 1
                },
                smooth: {
                    type: 'dynamic',
                    roundness: 0.5,
                    forceDirection: 'none'
                }
            },
            layout: {
                improvedLayout: false
            },
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 200,
                    updateInterval: 25
                },
                barnesHut: {
                    gravitationalConstant: -15000,
                    centralGravity: 0.1,
                    springLength: 250,
                    springConstant: 0.03,
                    damping: 0.95,
                    avoidOverlap: 1
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 300,
                zoomView: false,
                dragView: true,
                dragNodes: true
            }
        };

        // Apply node colors based on group - simplified approach
        const coloredNodes = graphData.nodes.map(node => ({
            id: node.id,
            label: node.label,
            title: node.title,
            x: node.x,
            y: node.y,
            color: config.visConfig.nodes[node.group].color,
        }));

        const network = new vis.Network(container, {
            nodes: new vis.DataSet(coloredNodes),
            edges: new vis.DataSet(graphData.edges)
        }, options);
        

        // Add legend
        addLegend();
        
        // Add refresh button
        addRefreshButton(network);
    }

    function addLegend() {
        const legendContainer = document.createElement('div');
        legendContainer.style.cssText = `
            position: absolute;
            top: 20px;
            left: 20px;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 15px;
            color: white;
            font-size: 12px;
            z-index: 1000;
        `;

        const legend = [
            { color: '#F59E0B', label: 'Data' },
            { color: '#10B981', label: 'CONTEXT' },
            { color: '#1d27efcf', label: 'Augmentation' },
            { color: '#EF4444', label: 'Function' },
            { color: '#8B5CF6', label: 'Storage' }
        ];

        let legendHTML = '';
        legend.forEach(item => {
            legendHTML += `
                <div style="display: flex; align-items: center; margin: 5px 0;">
                    <div style="width: 16px; height: 16px; border-radius: 50%; background: ${item.color}; margin-right: 8px; border: 2px solid white;"></div>
                    <span>${item.label}</span>
                </div>
            `;
        });

        legendContainer.innerHTML = legendHTML;
        document.getElementById('context-engineering-diagram').appendChild(legendContainer);
    }

    function addRefreshButton(network) {
        const refreshButton = document.createElement('button');
        refreshButton.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            border: 1px solid #555;
            border-radius: 50%;
            padding: 10px;
            font-size: 14px;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
        `;
        
        refreshButton.innerHTML = '<i class="fas fa-sync-alt"></i>';
        
        refreshButton.addEventListener('click', () => {
            refreshButton.innerHTML = '<i class="fas fa-check"></i>';
            initDiagram();
        });
        
        refreshButton.addEventListener('mouseenter', () => {
            refreshButton.style.transform = 'scale(1.05)';
        });
        
        refreshButton.addEventListener('mouseleave', () => {
            refreshButton.style.transform = 'scale(1)';
        });
        
        document.getElementById('context-engineering-diagram').appendChild(refreshButton);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initDiagram();
});