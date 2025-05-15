// script.js
const API_BASE = 'http://127.0.0.1:5000';

function addBook() {
  const book = {
    name: document.getElementById('bookName').value,
    author: document.getElementById('author').value,
    quantity: parseInt(document.getElementById('quantity').value),
    price: parseFloat(document.getElementById('price').value)
  };

  fetch(`${API_BASE}/add_book`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(book)
  }).then(res => res.json()).then(data => {
    document.getElementById('bookStatus').innerText = data.message;
  });
}

function sellBook() {
  const sale = {
    name: document.getElementById('sellBookName').value,
    quantity: parseInt(document.getElementById('sellQuantity').value),
    customer: document.getElementById('customerName').value,
    customer_number: document.getElementById('customerNumber').value
  };

  fetch(`${API_BASE}/sell_book`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(sale)
  }).then(res => res.json()).then(data => {
    document.getElementById('sellStatus').innerText = data.message;
  });
}

function getProfit() {
  fetch(`${API_BASE}/profit`).then(res => res.json()).then(data => {
    document.getElementById('todayProfit').innerText = `Today's Profit: ${data.today}`;
    document.getElementById('monthProfit').innerText = `This Month's Profit: ${data.month}`;
  });
}

function addStaff() {
  const staff = {
    emp_id: parseInt(document.getElementById('empId').value),
    name: document.getElementById('empName').value,
    salary: parseFloat(document.getElementById('salary').value),
    date: document.getElementById('joinDate').value,
    address: document.getElementById('address').value,
    mobile: document.getElementById('mobile').value
  };

  fetch(`${API_BASE}/add_staff`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(staff)
  }).then(res => res.json()).then(data => {
    document.getElementById('staffStatus').innerText = data.message;
  });
}

function deleteStaff() {
  const empId = document.getElementById('deleteEmpId').value;
  fetch(`${API_BASE}/delete_staff/${empId}`, {
    method: 'DELETE'
  }).then(res => res.json()).then(data => {
    document.getElementById('staffStatus').innerText = data.message;
  });
}

function searchBook() {
  const book = document.getElementById('searchBook').value;
  const author = document.getElementById('searchAuthor').value;

  fetch(`${API_BASE}/search_book?name=${book}&author=${author}`)
    .then(res => res.json())
    .then(data => {
      const resultDiv = document.getElementById('searchResult');
      if (data.length === 0) {
        resultDiv.innerHTML = '<p>No books found.</p>';
      } else {
        resultDiv.innerHTML = '<ul>' + data.map(b => `<li>${b.name} by ${b.author} - ${b.quantity} pcs at ₹${b.price}</li>`).join('') + '</ul>';
      }
    });
}
