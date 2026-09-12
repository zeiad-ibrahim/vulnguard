// Sample data for demonstration purposes
const sampleScanHistory = [
    { date: '2025-02-20', ip: '192.168.1.1', type: 'Full Scan', result: 'No vulnerabilities found' },
    { date: '2025-02-21', ip: '10.0.0.1', type: 'Targeted Scan (Ports: 22, 80)', result: 'Port 80: Vulnerability detected' },
    { date: '2025-02-22', ip: '172.16.0.5', type: 'Full Scan', result: 'No vulnerabilities found' }
];

// Function to populate the scan history table
function loadScanHistory() {
    const tableBody = document.getElementById('scanHistoryTable');
    tableBody.innerHTML = ''; // Clear existing rows

    sampleScanHistory.forEach(scan => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${scan.date}</td>
            <td>${scan.ip}</td>
            <td>${scan.type}</td>
            <td>${scan.result}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Load scan history when the page loads
window.onload = loadScanHistory;
