function SearchAndFilterThingy() {
  var input, filter, table, tr, td1, td2, x;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  table = document.getElementById("rosterTable");
  tr = table.getElementsByTagName("tr");

  for (x = 0; x < tr.length; x++) {
    td1 = tr[x].getElementsByTagName("td")[0];
    td2 = tr[x].getElementsByTagName("td")[1];
    if (td1 && td2) {
      if (td1.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[x].style.display = "";
      } else if (td2.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[x].style.display = "";
      } else {
        tr[x].style.display = "none";
      }
    }
  }
}