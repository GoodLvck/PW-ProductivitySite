document.addEventListener("submit", async (event) => {
    const form = event.target.closest(".subtask-toggle-form");

    if (!form) {
        return;
    }

    event.preventDefault();

    const submitButton = form.querySelector("button[type='submit']");
    submitButton.disabled = true;

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        if (!response.ok) {
            form.submit();
            return;
        }

        const html = await response.text();
        const currentList = document.getElementById("task-subtasks");
        currentList.outerHTML = html;
    } catch {
        form.submit();
    }
});
