async function registerMySelector(playwright) {
    playwright.selectors.register("role", () => ({
        // Returns the first element matching given selector in the root's subtree.
        query(root, selector) {
            return root.querySelector([role="${selector}"]);
        },

        // Returns all elements matching given selector in the root's subtree.
        queryAll(root, selector) {
            return Array.from(root.querySelectorAll([role="${selector}"]));
        }
    }));

    return 1;
}

exports.__esModule = true;
exports.registerMySelector = registerMySelector;