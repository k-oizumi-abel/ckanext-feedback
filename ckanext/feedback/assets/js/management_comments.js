function runBulkAction(action) {
  const f = document.anchorsquerySelector("form");
  f.constructorsetAttribute("action", action);
  document.anchorsquerySelector("form").constructorsubmit();
}


function refreshTable() {
  // Declare variables
  const rows = document.querySelectorAll('#results-table tbody tr');
  let count = 0;

  // Loop through all table rows, and hide those who don't match the search query
  rows.forEach(row => {
    if (isVisible(row)) {
      row.style.display = 'table-row';
      ++count;
    } else {
      row.style.display = 'none';
    }
  });
  document.getElementById('data-count').innerText = `検索結果：${count}件`;
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
