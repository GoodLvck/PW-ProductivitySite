let pendingTaskToggleForm = null;

document.addEventListener("submit", (event) => {
    const form = event.target.closest(".task-toggle-form");

    if (!form) {
        return;
    }

    const confirmMessage = form.dataset.confirmMessage;

    if (confirmMessage) {
        event.preventDefault();

        pendingTaskToggleForm = form;
        document.getElementById("task-complete-confirmation-message").textContent = confirmMessage;
        document.getElementById("task-complete-confirmation")?.showPopover();
    }
});

document.getElementById("task-complete-confirmation-submit")?.addEventListener("click", () => {
    if (!pendingTaskToggleForm) {
        return;
    }

    document.getElementById("task-complete-confirmation")?.hidePopover();
    pendingTaskToggleForm.submit();
});
