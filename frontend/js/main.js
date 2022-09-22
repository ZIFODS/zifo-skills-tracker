var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemePaired);

// Add "forces" to the simulation here
var simulation = d3.forceSimulation()
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("charge", d3.forceManyBody().strength(-20))
    .force("link", d3.forceLink().id(function(d) { return d.id; }).strength(0));

d3.json("data/skills_js.json").then(function(graph) {
    console.log(graph);

    simulation.force("r", d3.forceRadial(function(d) {
        if (d.group === "Consultant") {
            return 5
        }
        else {
            return 150
        }
        }, width/2, height/2)
    )

    // Add lines for every link in the dataset
    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

    // Add circles for every node in the dataset
    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
            .attr("r", 10)
            .attr("fill", function(d) { return color(d.group); })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended)
            );

    // Basic tooltips
    node.append("title")
        .text(function(d) { return d.name; });

    // Attach nodes to the simulation, add listener on the "tick" event
    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    // Associate the lines with the "link" force
    simulation.force("link")
        .links(graph.links)

    // Dynamically update the position of the nodes/links as time passes
    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
            }
        })

    .catch(function(error) {
        console.log(error)
    })

// Change the value of alpha, so things move around when we drag a node
function dragstarted(event, d) {
if (!event.active) simulation.alphaTarget(0.9).restart();
    d.fx = d.x;
    d.fy = d.y;
}

// Fix the position of the node that we are looking at
function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

// Let the node do what it wants again once we've looked at it
function dragended(event, d) {
if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// function group_dragstarted(group) {
//     if (!d3.event.active) simulation.alphaTarget(0.3).restart()
//     d3.select(this).select('path').style('stroke-width', 3);
// }

// function group_dragged(group) {
//     node
//       .filter(function(d) { return d.group == group; })
//       .each(function(d) {
//         d.x += d3.event.dx;
//         d.y += d3.event.dy;
//       })
//   }
  
//   function group_dragended(group) {
//     if (!d3.event.active) simulation.alphaTarget(0.3).restart();
//     d3.select(this).select('path').style('stroke-width', 1);
//   }