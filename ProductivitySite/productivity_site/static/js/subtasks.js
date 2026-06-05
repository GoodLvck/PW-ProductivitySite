document.addEventListener("submit", async (event) => {
    const form = event.target.closest(".subtask-toggle-form");

    if (!form) {
        return;
    }

    event.preventDefault();

    const button = form.querySelector(".subtask-toggle-icon");
    if (button) {
        button.disabled = true;
    }

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-Update-Task-Status": "true",
            },
        });

        if (!response.ok) {
            form.submit();
            return;
        }

        const contentType = response.headers.get("content-type") || "";
        const currentList = document.getElementById("task-subtasks");

        if (contentType.includes("application/json")) {
            const data = await response.json();
            const taskStatusContainer = document.getElementById("task-status-container");

            if (taskStatusContainer && data.task_status_html) {
                taskStatusContainer.innerHTML = data.task_status_html;
            }

            if (currentList && data.subtask_list_html) {
                currentList.outerHTML = data.subtask_list_html;
            }
            return;
        }

        const html = await response.text();
        if (currentList) {
            currentList.outerHTML = html;
        }
    } catch {
        form.submit();
    } finally {
        if (button) {
            button.disabled = false;
        }
    }
});
