document.addEventListener('DOMContentLoaded', function () {
    function autoScale() {
        const elements = document.querySelectorAll('.auto-sizing');

        elements.forEach(element => {
            const container = element.parentElement;

            // 重置transform以获取内容的自然尺寸
            element.style.transform = 'scale(1)';
            element.style.width = 'auto';
            element.style.height = 'auto';

            // 获取内容和容器的宽高
            const contentHeight = element.scrollHeight;
            const containerHeight = container.clientHeight;
            const contentWidth = element.scrollWidth;
            const containerWidth = container.clientWidth;

            // 获取容器和内容的实际位置
            const containerRect = container.getBoundingClientRect();
            const contentRect = element.getBoundingClientRect();

            // 计算偏移量
            const offsetX = contentRect.left - containerRect.left;
            const offsetY = contentRect.top - containerRect.top;

            // 获取容器的内边距
            const computedStyle = window.getComputedStyle(container);
            const paddingLeft = parseFloat(computedStyle.paddingLeft);
            const paddingRight = parseFloat(computedStyle.paddingRight);
            const paddingTop = parseFloat(computedStyle.paddingTop);
            const paddingBottom = parseFloat(computedStyle.paddingBottom);

            // 计算实际可用空间
            const availableWidth = containerWidth - paddingLeft - paddingRight - offsetX;
            const availableHeight = containerHeight - paddingTop - paddingBottom - offsetY;

            // 计算高度缩放比例
            let scale = availableHeight / contentHeight;

            // 根据高度缩放比例调整内容宽度
            if (scale < 1 || contentWidth > availableWidth) {
                element.style.transform = `scale(${scale})`;
                element.style.width = `${availableWidth / scale}px`;
                element.style.height = `${availableHeight / scale}px`;
            } else {
                element.style.width = '100%';
                element.style.height = '100%';
            }
        });
    }

    // 初始调用
    autoScale();

    // 在窗口大小改变时再次调用
    window.addEventListener('resize', autoScale);
});