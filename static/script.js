/**
 * Core UI Logic Scripting binding generic JS operations natively
 */

async function copyFixText(text) {
    try {
        await navigator.clipboard.writeText(text);
        
        const copyBtns = document.querySelectorAll('.btn-copy');
        copyBtns.forEach(btn => {
            const originalText = btn.innerHTML;
            btn.innerHTML = "Copied ✓";
            btn.style.backgroundColor = "var(--text-primary)";
            btn.style.color = "var(--bg-panel)";
            btn.style.borderColor = "var(--text-primary)";
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.backgroundColor = "";
                btn.style.color = "";
                btn.style.borderColor = "";
            }, 1500);
        });
    } catch (err) {
        console.error('Failed to copy text:', err);
    }
}
