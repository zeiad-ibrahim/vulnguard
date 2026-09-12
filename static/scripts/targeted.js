document.getElementById('startTargetedScan').addEventListener('click', () => {
    const ipAddress = document.getElementById('ipAddress').value.trim();
    const ports = document.getElementById('ports').value.trim();
    const status = document.getElementById('scanStatus');
    const resultsContainer = document.getElementById('scanResults');

    // IP address validation
    const ipPattern = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

    // Port validation (single number only)
    const portPattern = /^\d{1,5}$/;

    if (!ipPattern.test(ipAddress)) {
        status.textContent = 'Invalid IP Address. Please enter a valid IP address.';
        status.style.color = 'red';
        return;
    }

    if (!portPattern.test(ports)) {
        status.textContent = 'Invalid Port. Please enter a single valid port number (e.g., 22, 80, 443).';
        status.style.color = 'red';
        return;
    }

    status.style.color = '#555';
    status.textContent = `Scanning ${ipAddress} on port ${ports}... Please wait.`;

    // Send request to backend
    fetch('/targeted_scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ipAddress, ports })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            status.textContent = `Scan Complete! Results for ${ipAddress}:`;

            let resultHTML = '<h3>Scan Results:</h3>';
            if (data.results.length > 0) {
                data.results.forEach(result => {
                    resultHTML += `
                        <p><strong>${result.port_info}</strong></p>
                        <p><strong>Vulnerabilities:</strong> ${result.vulnerabilities.join(', ')}</p>
                        <p><strong>Recommendations:</strong> ${result.recommendations.join(', ')}</p>
                        <hr>
                    `;
                });
            } else {
                resultHTML += `<p>No open ports found for ${ipAddress} on port ${ports}.</p>`;
            }

            resultsContainer.innerHTML = resultHTML;
        } else {
            status.textContent = `Error: ${data.error}`;
            status.style.color = 'red';
        }
    })
    .catch(error => {
        status.textContent = `Error: Failed to connect to the scanning service.`;
        status.style.color = 'red';
        console.error('Error:', error);
    });
});
