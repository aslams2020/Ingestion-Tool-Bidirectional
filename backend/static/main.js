document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn, .tab-content').forEach(el => {
                el.classList.remove('active');
            });
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // ClickHouse Connection
    document.getElementById('ch-connect').addEventListener('click', async () => {
        const config = {
            host: document.getElementById('ch-host').value || 'localhost',
            port: parseInt(document.getElementById('ch-port').value) || 9000,
            database: document.getElementById('ch-db').value || 'default',
            user: document.getElementById('ch-user').value,
            password: document.getElementById('ch-pass').value,
            jwt_token: document.getElementById('ch-jwt').value
        };
    
        try {
            const response = await fetch('/api/connect/clickhouse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Connection failed');
            }
            
            updateStatus('Connected successfully!');
            document.getElementById('schema-section').style.display = 'block';
            
        } catch (error) {
            updateStatus(`Error: ${error.message}`, 'error');
            console.error('Connection error:', error);
        }
    });
    // Schema loading and column selection
    async function loadTables() {
        try {
            const response = await fetch('/api/schema/discover', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_type: 'clickhouse' })
            });
            const data = await response.json();
            
            const tableSelect = document.getElementById('table-selection');
            tableSelect.innerHTML = data.tables.map(table => `
                <div class="table-item">
                    <input type="checkbox" id="table-${table}" value="${table}">
                    <label for="table-${table}">${table}</label>
                </div>
            `).join('');
            
            // Add event listeners for table selection
            document.querySelectorAll('#table-selection input').forEach(input => {
                input.addEventListener('change', loadColumns);
            });
        } catch (error) {
            updateStatus(`Failed to load tables: ${error.message}`, 'error');
        }
    }
    
});