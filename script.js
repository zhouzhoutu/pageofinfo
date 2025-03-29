// 处理表单提交
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = form.querySelector('input[type="text"]').value;
            const email = form.querySelector('input[type="email"]').value;
            const message = form.querySelector('textarea').value;
            
            // 这里可以添加表单验证
            if (!name || !email || !message) {
                alert('请填写所有必填字段');
                return;
            }
            
            // 这里可以添加发送表单数据的逻辑
            console.log('表单提交:', { name, email, message });
            alert('感谢您的留言，我们会尽快回复！');
            form.reset();
        });
    }

    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    const searchInput = document.getElementById('searchInput');
    const linkCards = document.querySelectorAll('.link-card');

    // 搜索功能
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        
        linkCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('p').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // 添加链接点击效果
    linkCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // 如果链接是外部链接，在新标签页中打开
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                e.preventDefault();
                window.open(this.getAttribute('href'), '_blank');
            }
        });
    });

    // 添加页面加载动画
    document.body.classList.add('loaded');
});

// 添加导航栏滚动效果
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll) {
        header.style.transform = 'translateY(-100%)';
    } else {
        header.style.transform = 'translateY(0)';
    }
    lastScroll = currentScroll;
}); 