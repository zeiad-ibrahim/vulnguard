// Add an event listener to the full scan form to handle submission
document.getElementById("fullScanForm").addEventListener("submit", function(event) {
    const status = document.getElementById('scanStatus');
    
    // Prevent the form from submitting immediately
    event.preventDefault();

    // Get the IP address input and remove extra spaces
    var ipAddress = document.getElementById("ipAddress").value.trim();
    // Get the results div to display scan results
    var resultsDiv = document.getElementById("scanResults");

    // Validate IP address format (basic regex for IPv4)
    var ipPattern = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    if (!ipPattern.test(ipAddress)) {
        resultsDiv.innerHTML = '<p style="color: red;">Please enter a valid IP address (e.g., 192.168.1.1).</p>';
        return;
    }


    status.style.color = '#555';
    status.textContent = `Scanning ${ipAddress} ...`
    // Send the IP address to the server for scanning
    fetch('/full_scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ipAddress: ipAddress })
    })
    // Convert the server response to JSON
    .then(function(response) { return response.json(); })
    // Handle the server's response
    .then(function(data) {
        if (data.success) {
            // Display the scan results
            status.textContent = `Scan Completed!`;
            var resultsHTML = '<h3>Scan Results for ' + ipAddress + '</h3>';
            if (data.results.length === 0) {
                resultsHTML += '<p>No open ports found.</p>';
            } else {
                resultsHTML += '<ul>';
                data.results.forEach(function(result) {
                    resultsHTML += '<li>';
                    resultsHTML += '<strong>' + result.port_info + '</strong><br>';
                    if (result.vulnerabilities.length > 0) {
                        resultsHTML += 'Potential Vulnerabilities: ' + result.vulnerabilities.join(', ') + '<br>';
                        resultsHTML += 'Recommendations: ' + result.recommendations.join(', ');
                    } else {
                        resultsHTML += 'No known vulnerabilities for this port.';
                    }
                    resultsHTML += '</li>';
                });
                resultsHTML += '</ul>';
            }
            resultsDiv.innerHTML = resultsHTML;
        } else {
            resultsDiv.innerHTML = '<p style="color: red;">' + data.error + '</p>';
        }
    })
    // Handle any network or server errors
    .catch(function(error) {
        resultsDiv.innerHTML = '<p style="color: red;">Something went wrong. Try again.</p>';
        console.log("Error:", error);
    });
});