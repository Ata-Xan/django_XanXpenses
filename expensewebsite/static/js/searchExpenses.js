const appTable = document.querySelector(".app-table");
const pagination = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");


document.addEventListener("DOMContentLoaded", function () {
    var searchField = document.getElementById("searchField");
    searchField.addEventListener("keyup", function () {
        var value = searchField.value.toLowerCase();
        var xhr = new XMLHttpRequest();
        var notFound = 0;
        xhr.open("POST", "/search-expenses/");
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                var expenseTableBody = document.querySelector("table tbody");
                expenseTableBody.innerHTML = "";
                if (data.results.length > 0) {
                    notFound = 0;
                    noResults.style.display = 'none';
                    appTable.style.display = 'block';
                    pagination.style.display = 'block';
                    results = data.results;

                    results.forEach(function (expense) {
                        var row = document.createElement("tr");
                        var deleteURL = "/delete_expense/" + expense.id;
                        var editURL = "/edit-expense/" + expense.id;
                        row.innerHTML = "<td>" + expense.amount + "</td><td>" + expense.category + "</td><td>" + expense.description + "</td><td>" + expense.date + "</td>" + `<td>
                                <div class="d-flex justify-content-between">
                                    <a href=${editURL}
                                       class="btn btn-primary btn-sm flex-fill mr-2">
                                        <i class="bi bi-pencil-square"></i> Edit
                                    </a>
                                    <button type="button" class="btn btn-danger btn-sm flex-fill"
                                            data-toggle="modal"
                                            data-target="#confirm-delete-modal" id="delete-btn">
                                        <i class="bi bi-trash"></i> Delete
                                    </button>
                                </div>
                                <div class="modal fade" id="confirm-delete-modal" tabindex="-1" role="dialog"
                                     aria-labelledby="confirm-delete-modal-label" aria-hidden="true">
                                    <div class="modal-dialog" role="document">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="confirm-delete-modal-label">Confirm
                                                    deletion</h5>
                                                <button type="button" class="close" data-dismiss="modal"
                                                        aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                            </div>
                                            <div class="modal-body">
                                                Are you sure you want to delete this item?
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary"
                                                        data-dismiss="modal">
                                                    Cancel
                                                </button>
                                                <a href=${deleteURL}
                                                   class="btn btn-danger">Yes</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
`;
                        expenseTableBody.appendChild(row);
                    });


                } else {
                    notFound = 1;
                    noResults.style.display = 'block';
                    appTable.style.display = 'none';
                    pagination.style.display = 'none';
                }


            }
        };
        xhr.send("search=" + value);
    });
});
