const utilizationCheckboxAll = document.getElementById("utilization-comments-checkbox-all");
utilizationCheckboxAll.addEventListener('change', changeAllChekbox);

function changeAllChekbox(e) {
  let rows;
  if (e.target.id === 'utilization-comments-checkbox-all') {
    rows = document.querySelectorAll('#utilization-comments-table tbody tr');
  } else if (e.target.id === 'resource-comments-checkbox-all') {
    rows = document.querySelectorAll('#resource-comments-table tbody tr');
  }
  Array.from(rows).filter(row => isVisible(row)).forEach(row => {
    row.querySelector('input[type="checkbox"]').checked = e.target.checked;
  });
}


function runBulkAction(action) {
  const form = document.getElementById("comments-form");
  form.setAttribute("action", action);
  form.submit();
}


function refreshTable() {
  // Declare variables
  const rows = document.querySelectorAll('tbody tr');
  let count = 0;

  rows.forEach(row => {
    if (isVisible(row)) {
      row.style.display = 'table-row';
      ++count;
    } else {
      row.style.display = 'none';
      row.querySelector('input[type="checkbox"]').checked = false;
    }
  });
  document.getElementById('utilization-comments-results-count').innerText = count;
}

function isVisible(row){
  const statusCell = row.getElementsByTagName('td')[7];
  const isWaiting = document.getElementById('waiting').checked && statusCell.dataset.waiting;
  const isApproval = document.getElementById('approval').checked && statusCell.dataset.approval;
  const categoryCell = row.getElementsByTagName('td')[5];
  const categories = Array.from(document.querySelectorAll('.category-checkbox'));
  const isMatchedCategory = categories.filter(element => element.checked)
                                      .some(element => element.getAttribute('name') === categoryCell.getInnerHTML());
  return (isWaiting || isApproval) && isMatchedCategory;
}