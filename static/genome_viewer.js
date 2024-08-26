// Sample data: replace this with actual genome data
const genomeData = [
    { position: 100, label: "Gene 1" },
    { position: 300, label: "Gene 2" },
    { position: 600, label: "Gene 3" },
    { position: 1000, label: "Gene 4" },
];

const width = document.getElementById('viewer').clientWidth;
const height = document.getElementById('viewer').clientHeight;
const padding = 50;

// Check dimensions
console.log(`Width: ${width}, Height: ${height}`);

// Create an SVG element
const svg = d3.select("#viewer")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Create a scale for the x-axis based on the genome positions
const xScale = d3.scaleLinear()
    .domain([0, 1500])  // Replace 1500 with the maximum genome position
    .range([padding, width - padding]);

// Create the x-axis
const xAxis = d3.axisBottom(xScale)
    .ticks(10);

svg.append("g")
    .attr("transform", `translate(0,${height - padding})`)
    .call(xAxis);

// Plot the markers on the timeline
svg.selectAll("circle")
    .data(genomeData)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.position))
    .attr("cy", height / 2)
    .attr("r", 10)
    .style("fill", "red");

// Add labels to the markers
svg.selectAll("text")
    .data(genomeData)
    .enter()
    .append("text")
    .attr("x", d => xScale(d.position))
    .attr("y", (height / 2) - 15)
    .attr("text-anchor", "middle")
    .text(d => d.label)
    .style("font-size", "12px")
    .style("fill", "#333");

// Add interactivity: clicking on the viewer adds a new marker
svg.on("click", function(event) {
    const [x] = d3.pointer(event);
    const newPos = xScale.invert(x);

    svg.append("circle")
        .attr("cx", x)
        .attr("cy", height / 2)
        .attr("r", 10)
        .style("fill", "red");

    svg.append("text")
        .attr("x", x)
        .attr("y", (height / 2) - 15)
        .attr("text-anchor", "middle")
        .text(`Pos: ${Math.round(newPos)}`)
        .style("font-size", "12px")
        .style("fill", "#333");
});

