// JavaScript for Bill Creation and Update

let items = [];
let oldGoldItems = [];

// Add item row
function addItem(itemData = null) {
    const tbody = document.getElementById('items-table-body');
    const row = document.createElement('tr');
    
    // Get gold rate, silver rate, and bar rate from hidden inputs or default
    const goldRateInput = document.getElementById('gold-rate-input');
    const silverRateInput = document.getElementById('silver-rate-input');
    const barRateInput = document.getElementById('bar-rate-input');
    const defaultGoldRate = goldRateInput ? goldRateInput.value : '0';
    const defaultSilverRate = silverRateInput ? silverRateInput.value : '0';
    const defaultBarRate = barRateInput ? barRateInput.value : '0';
    
    const item = itemData || {
        item_type: 'S',
        material_type: 'gold',
        description: '',
        item_code: '',
        item_number: '',
        net_weight: '',
        tunch_wstg: '91.60',
        labour: '0',
        rate: defaultGoldRate
    };
    
    // Determine default rate based on material type
    let defaultRate = defaultGoldRate;
    if (item.material_type === 'silver') {
        defaultRate = defaultSilverRate;
    } else if (item.material_type === 'bar') {
        defaultRate = defaultBarRate;
    }
    
    // Update rate if not already set
    if (!item.rate || item.rate === '0' || item.rate === 0) {
        item.rate = defaultRate;
    }
    
    row.innerHTML = `
        <td>
            <select class="form-control form-control-sm mb-1" 
                    onchange="updateItem(this, 'item_type')" 
                    style="font-size: 0.75rem;">
                <option value="S" ${item.item_type === 'S' ? 'selected' : ''}>S</option>
                <option value="REC" ${item.item_type === 'REC' ? 'selected' : ''}>REC</option>
            </select>
            <select class="form-control form-control-sm mb-1" 
                    onchange="updateItem(this, 'material_type')" 
                    style="font-size: 0.75rem;">
                <option value="gold" ${item.material_type === 'gold' ? 'selected' : ''}>Gold</option>
                <option value="silver" ${item.material_type === 'silver' ? 'selected' : ''}>Silver</option>
                <option value="bar" ${item.material_type === 'bar' ? 'selected' : ''}>Bar</option>
            </select>
            <input type="text" class="form-control form-control-sm" 
                   value="${item.description || ''}" 
                   onchange="updateItem(this, 'description')" 
                   placeholder="Item description">
            <input type="text" class="form-control form-control-sm mt-1" 
                   value="${item.item_code || ''}" 
                   onchange="updateItem(this, 'item_code')" 
                   placeholder="Item Code" style="font-size: 0.75rem;">
            <input type="text" class="form-control form-control-sm mt-1" 
                   value="${item.item_number || ''}" 
                   onchange="updateItem(this, 'item_number')" 
                   placeholder="Item No (e.g., 5570)" style="font-size: 0.75rem;">
        </td>
        <td>
            <input type="number" step="0.001" min="0.001" class="form-control form-control-sm" 
                   value="${item.net_weight || ''}" 
                   onchange="updateItem(this, 'net_weight')" 
                   placeholder="0.000">
        </td>
        <td>
            <input type="number" step="0.01" min="0.000001" class="form-control form-control-sm" 
                   value="${item.tunch_wstg || '91.60'}" 
                   onchange="updateItem(this, 'tunch_wstg')" 
                   placeholder="91.60">
        </td>
        <td>
            <input type="number" step="0.01" min="0" class="form-control form-control-sm" 
                   value="${item.labour || '0'}" 
                   onchange="updateItem(this, 'labour')" 
                   placeholder="Labour">
        </td>
        <td>
            <input type="number" step="0.01" min="0.01" class="form-control form-control-sm" 
                   value="${item.rate || defaultRate}" 
                   onchange="updateItem(this, 'rate')" 
                   placeholder="Rate">
        </td>
        <td class="s-fine-cell text-end">0.000</td>
        <td class="g-fine-cell text-end">0.000</td>
        <td class="amount-cell">₹ 0.00</td>
        <td>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeItem(this)">
                <i class="fas fa-times"></i>
            </button>
        </td>
    `;
    
    tbody.appendChild(row);
    updateItemCalculations(row);
    updateTotals();
}

// Update item field
function updateItem(input, field) {
    const row = input.closest('tr');
    const index = Array.from(row.parentNode.children).indexOf(row);
    
    if (!items[index]) {
        items[index] = {};
    }
    
    items[index][field] = input.value;
    
    // If material_type changed, update rate accordingly
    if (field === 'material_type') {
        const materialType = input.value;
        const goldRateInput = document.getElementById('gold-rate-input');
        const silverRateInput = document.getElementById('silver-rate-input');
        const barRateInput = document.getElementById('bar-rate-input');
        const rateInput = row.querySelector('input[onchange*="rate"]');
        
        if (rateInput) {
            let newRate = '0';
            if (materialType === 'gold' && goldRateInput) {
                newRate = goldRateInput.value || '0';
            } else if (materialType === 'silver' && silverRateInput) {
                newRate = silverRateInput.value || '0';
            } else if (materialType === 'bar' && barRateInput) {
                newRate = barRateInput.value || '0';
            }
            
            rateInput.value = newRate;
            items[index]['rate'] = newRate;
        }
    }
    
    updateItemCalculations(row);
    updateTotals();
}

// Update item calculations
function updateItemCalculations(row) {
    const netWeight = parseFloat(row.querySelector('input[onchange*="net_weight"]')?.value || 0);
    const tunchWstg = parseFloat(row.querySelector('input[onchange*="tunch_wstg"]')?.value || 0);
    const rate = parseFloat(row.querySelector('input[onchange*="rate"]')?.value || 0);
    const labour = parseFloat(row.querySelector('input[onchange*="labour"]')?.value || 0);
    
    const materialType = row.querySelector('select[onchange*="material_type"]')?.value || 'gold';
    let gFine = 0;
    let sFine = 0;
    let metalAmount = 0;

    // Fine calculation uses Net weight × Tunch wstg / 100 via calculateFineGold
    if (materialType === 'gold') {
        gFine = calculateFineGold(netWeight, tunchWstg);
        sFine = 0;
        metalAmount = calculateAmount(gFine, rate);
    } else if (materialType === 'silver') {
        sFine = calculateFineGold(netWeight, tunchWstg);
        gFine = 0;
        metalAmount = calculateAmount(sFine, rate);
    
    } else {
        // bar or other material: no fine by default
        gFine = 0;
        sFine = 0;
        metalAmount = 0;
    }

    const amount = metalAmount + labour;
    
    // Update fine cells
    const sFineCell = row.querySelector('.s-fine-cell');
    const gFineCell = row.querySelector('.g-fine-cell');
    if (sFineCell) {
        sFineCell.textContent = sFine.toFixed(3);
    }
    if (gFineCell) {
        gFineCell.textContent = gFine.toFixed(3);
    }
    if (row.querySelector('.amount-cell')) {
        row.querySelector('.amount-cell').textContent = formatCurrency(amount);
    }
    
    // Update items array
    const index = Array.from(row.parentNode.children).indexOf(row);
    if (!items[index]) {
        items[index] = {};
    }
    items[index].g_fine = gFine;
    items[index].s_fine = sFine;
    items[index].amount = amount;
}

// Remove item
function removeItem(button) {
    const row = button.closest('tr');
    const index = Array.from(row.parentNode.children).indexOf(row);
    items.splice(index, 1);
    row.remove();
    updateTotals();
}

// Add old gold
function addOldGold() {
    const weight = parseFloat(document.getElementById('old-gold-weight').value || 0);
    const rate = parseFloat(document.getElementById('old-gold-rate').value || 0);
    const desc = document.getElementById('old-gold-desc').value || '';
    
    if (weight <= 0 || rate <= 0) {
        alert('Please enter valid weight and rate');
        return;
    }
    
    const value = weight * rate;
    const oldGold = { weight, rate_per_gram: rate, description: desc, value };
    oldGoldItems.push(oldGold);
    
    // Add to UI
    const list = document.getElementById('old-gold-list');
    const div = document.createElement('div');
    div.className = 'old-gold-item mb-2 p-2 border rounded';
    div.innerHTML = `
        <div class="d-flex justify-content-between">
            <div>
                <strong>${weight.toFixed(3)} gm</strong> @ ₹${rate.toFixed(2)} = ₹${value.toFixed(2)}
                ${desc ? '<br><small>' + desc + '</small>' : ''}
            </div>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeOldGold(this)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    list.appendChild(div);
    
    // Clear inputs
    document.getElementById('old-gold-weight').value = '';
    document.getElementById('old-gold-desc').value = '';
    
    updateTotals();
}

// Remove old gold
function removeOldGold(button) {
    const div = button.closest('.old-gold-item');
    const index = Array.from(div.parentNode.children).indexOf(div);
    oldGoldItems.splice(index, 1);
    div.remove();
    updateTotals();
}

// Update totals
function updateTotals() {
    // Collect all items from table
    const rows = document.querySelectorAll('#items-table-body tr');
    items = [];
    let totalFineGold = 0;
    let totalFineSilver = 0;
    let totalAmount = 0;
    
    rows.forEach(row => {
        const itemType = row.querySelector('select[onchange*="item_type"]')?.value || 'S';
        const materialType = row.querySelector('select[onchange*="material_type"]')?.value || 'gold';
        const netWeight = parseFloat(row.querySelector('input[onchange*="net_weight"]')?.value || 0);
        const tunchWstg = parseFloat(row.querySelector('input[onchange*="tunch_wstg"]')?.value || 0);
        const rate = parseFloat(row.querySelector('input[onchange*="rate"]')?.value || 0);
        const labour = parseFloat(row.querySelector('input[onchange*="labour"]')?.value || 0);
        const description = row.querySelector('input[onchange*="description"]')?.value || '';
        const itemCode = row.querySelector('input[onchange*="item_code"]')?.value || '';
        const itemNumber = row.querySelector('input[onchange*="item_number"]')?.value || '';
        
        let gFine = 0;
        let sFine = 0;
        let metalAmount = 0;
        if (materialType === 'gold') {
            gFine = calculateFineGold(netWeight, tunchWstg);
            sFine = 0;
            metalAmount = calculateAmount(gFine, rate);
        } else if (materialType === 'silver') {
            sFine = calculateFineGold(netWeight, tunchWstg);
            gFine = 0;
            metalAmount = calculateAmount(sFine, rate);
        } else {
            gFine = 0;
            sFine = 0;
            metalAmount = 0;
        }
        const amount = metalAmount + labour;
        
        items.push({
            item_type: itemType,
            material_type: materialType,
            description,
            item_code: itemCode,
            item_number: itemNumber,
            net_weight: netWeight,
            tunch_wstg: tunchWstg,
            labour: labour,
            rate: rate,
            s_fine: sFine,
            g_fine: gFine,
            amount: amount
        });
        
        totalFineGold += gFine;
        totalFineSilver += sFine;
        totalAmount += amount;
    });
    
    // Calculate old gold total
    const totalOldGoldValue = oldGoldItems.reduce((sum, og) => sum + og.value, 0);
    
    // Calculate tax (on taxable amount)
    const taxableAmount = totalAmount - totalOldGoldValue;
    const cgstPercent = parseFloat(document.querySelector('#id_cgst_percent')?.value || 1.5);
    const sgstPercent = parseFloat(document.querySelector('#id_sgst_percent')?.value || 1.5);
    const cgstAmount = (taxableAmount * cgstPercent) / 100;
    const sgstAmount = (taxableAmount * sgstPercent) / 100;
    
    // Calculate net payable
    const netPayable = totalAmount + cgstAmount + sgstAmount - totalOldGoldValue;
    
    // Update display
    if (document.getElementById('total-fine-gold')) {
        document.getElementById('total-fine-gold').textContent = totalFineGold.toFixed(3);
    }
    if (document.getElementById('total-s-fine')) {
        document.getElementById('total-s-fine').textContent = totalFineSilver.toFixed(3);
    }
    if (document.getElementById('total-amount')) {
        document.getElementById('total-amount').textContent = formatCurrency(totalAmount);
    }
    
    if (document.getElementById('summary-fine-gold')) {
        document.getElementById('summary-fine-gold').textContent = totalFineGold.toFixed(3) + ' gm';
        document.getElementById('summary-gross').textContent = formatCurrency(totalAmount);
        document.getElementById('summary-old-gold').textContent = formatCurrency(totalOldGoldValue);
        document.getElementById('summary-cgst').textContent = formatCurrency(cgstAmount);
        document.getElementById('summary-sgst').textContent = formatCurrency(sgstAmount);
        document.getElementById('summary-net-payable').textContent = formatCurrency(netPayable);
    }
    
    // Validate cash received doesn't exceed net payable
    const cashReceivedInput = document.querySelector('#id_cash_received');
    if (cashReceivedInput) {
        const cashReceived = parseFloat(cashReceivedInput.value || 0);
        if (cashReceived > netPayable) {
            cashReceivedInput.setCustomValidity(`Cash received cannot exceed net payable (₹${netPayable.toFixed(2)})`);
            cashReceivedInput.classList.add('is-invalid');
        } else {
            cashReceivedInput.setCustomValidity('');
            cashReceivedInput.classList.remove('is-invalid');
        }
    }
}

// Submit form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bill-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Calculate net payable first
            updateTotals();
            
            // Get net payable from summary
            const summaryNetPayable = document.getElementById('summary-net-payable');
            let netPayable = 0;
            if (summaryNetPayable) {
                const text = summaryNetPayable.textContent.replace(/[₹,\s]/g, '');
                netPayable = parseFloat(text) || 0;
            }
            
            // Validate cash received
            const cashReceivedInput = document.querySelector('#id_cash_received');
            if (cashReceivedInput) {
                const cashReceived = parseFloat(cashReceivedInput.value || 0);
                if (cashReceived > netPayable) {
                    e.preventDefault();
                    alert(`Cash received (₹${cashReceived.toFixed(2)}) cannot exceed net payable (₹${netPayable.toFixed(2)}).`);
                    cashReceivedInput.focus();
                    return false;
                }
            }
            
            // Update hidden inputs with JSON data
            document.getElementById('items-data').value = JSON.stringify(items);
            document.getElementById('old-gold-data').value = JSON.stringify(oldGoldItems);
        });
    }
    
    // Add event listeners for tax fields and cash received
    const cgstField = document.querySelector('#id_cgst_percent');
    const sgstField = document.querySelector('#id_sgst_percent');
    const cashReceivedField = document.querySelector('#id_cash_received');
    if (cgstField) cgstField.addEventListener('change', updateTotals);
    if (sgstField) sgstField.addEventListener('change', updateTotals);
    if (cashReceivedField) {
        cashReceivedField.addEventListener('input', updateTotals);
        cashReceivedField.addEventListener('change', updateTotals);
    }
});

// Helper function to add item row (for update page)
function addItemRow(itemData) {
    addItem(itemData);
}

