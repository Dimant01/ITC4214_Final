document.addEventListener("DOMContentLoaded", function () {

    const MOBILE_BREAKPOINT = 900;

    function setPageSize() {
        const width = window.innerWidth;

        // Decide page size based on window width
        let pageSize;

        if (width <= MOBILE_BREAKPOINT) {
            pageSize = 4;
        } else if (width <= 1200) {
            pageSize = 8;
        } else {
            pageSize = 12;
        }

        applyPageSize(pageSize);
    }

    function applyPageSize(size) {
        const url = new URL(window.location.href);

        // only update if changed
        if (url.searchParams.get("page_size") !== String(size)) {
            url.searchParams.set("page_size", size);
            window.location.href = url.toString();
        }
    }

    // -------------------------
    // DEBOUNCE FUNCTION
    // -------------------------
    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    const handleResize = debounce(function () {
        setPageSize();
    }, 300);

    window.addEventListener("resize", handleResize);

    // initial run
    setPageSize();
});