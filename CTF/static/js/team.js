document.addEventListener('DOMContentLoaded', () => {
    const copyBtn = document.getElementById('copy-invite-code');
    copyBtn.addEventListener('click', () => {
        const inviteCode = copyBtn.dataset.invite;
        navigator.clipboard.writeText(inviteCode).then(() => {
            alert('کد دعوت تیم کپی شد: ' + inviteCode);
        }).catch(err => {
            console.error('کپی انجام نشد:', err);
        });
    });
});