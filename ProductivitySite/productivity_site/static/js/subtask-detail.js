document.addEventListener("submit", async (event) => {
    const form = event.target.closest(".subtask-status-form");

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
                "X-Subtask-Detail": "true",
            },
        });

        if (!response.ok) {
            form.submit();
            return;
        }

        const html = await response.text();
        form.outerHTML = html;
    } catch {
        form.submit();
    }
});
