let valueType = document.getElementById('value-type').value;

async function loadData() {
    const type = valueType;
    const tbody = document.querySelector('#data-table tbody');
    const status = document.getElementById('status');
    const select = document.getElementById('value-type');
    document.getElementById('value-header').textContent = `${select.selectedOptions[0].text} Value`;
    try {
        const res = await fetch(`/api/${type}`);
        if (!res.ok) throw new Error(res.statusText);
        const rows = await res.json();
        if (type !== valueType) return;

        tbody.innerHTML = '';
        for (const row of rows) {
            const tr = document.createElement('tr');
            const cells = [
                row.id,
                new Date(row.recorded_at).toLocaleString(),
                row[`${type}_value`],
                row.sensor_id,
                row.loc,
            ];
            for (const value of cells) {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        }
        status.textContent = rows.length ? '' : 'No data yet.';
    } catch (err) {
        if (type !== valueType) return;
        status.textContent = 'Failed to load data: ' + err.message;
    }
}

loadData();

document.getElementById('value-type').addEventListener('change', () => {
    valueType = document.getElementById('value-type').value;
    loadData();
});
setInterval(loadData, 5000);
