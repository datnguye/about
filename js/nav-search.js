(function () {
    var toggle = document.getElementById('search-toggle');
    var field = document.getElementById('search-field');
    if (!toggle || !field) return;

    function openSearch() {
        field.classList.remove('hidden');
        field.classList.add('block', 'search-field-mobile');
        toggle.setAttribute('aria-expanded', 'true');
        var input = document.getElementById('search-input');
        if (input) input.focus();
    }

    function closeSearch() {
        field.classList.add('hidden');
        field.classList.remove('block', 'search-field-mobile');
        toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function (e) {
        e.stopPropagation();
        if (toggle.getAttribute('aria-expanded') === 'true') {
            closeSearch();
        } else {
            openSearch();
        }
    });

    document.addEventListener('click', function (e) {
        if (toggle.getAttribute('aria-expanded') !== 'true') return;
        if (!field.contains(e.target) && !toggle.contains(e.target)) {
            closeSearch();
        }
    });

    var mq = window.matchMedia('(min-width: 768px)');
    function syncToBreakpoint(ev) {
        if (ev.matches) {
            field.classList.remove('hidden', 'block', 'search-field-mobile');
            toggle.setAttribute('aria-expanded', 'false');
        } else if (toggle.getAttribute('aria-expanded') !== 'true') {
            field.classList.add('hidden');
        }
    }
    mq.addEventListener('change', syncToBreakpoint);
})();
