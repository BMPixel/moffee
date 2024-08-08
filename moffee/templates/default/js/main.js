// Automatic resizing to fit elements
window.addEventListener('load', function () {
    function autoScale() {
        const elements = document.querySelectorAll('.auto-sizing');

        elements.forEach(element => {
            const container = element.parentElement;

            // Reset transform for real dimensions
            element.style.transform = 'scale(1)';
            element.style.width = 'auto';
            element.style.height = 'auto';

            const contentHeight = element.scrollHeight;
            const containerHeight = container.clientHeight;
            const contentWidth = element.scrollWidth;
            const containerWidth = container.clientWidth;

            // Element may not align with container
            const containerRect = container.getBoundingClientRect();
            const contentRect = element.getBoundingClientRect();
            const offsetX = contentRect.left - containerRect.left;
            const offsetY = contentRect.top - containerRect.top;

            // Consider padding
            const computedStyle = window.getComputedStyle(container);
            const paddingLeft = parseFloat(computedStyle.paddingLeft);
            const paddingRight = parseFloat(computedStyle.paddingRight);
            const paddingTop = parseFloat(computedStyle.paddingTop);
            const paddingBottom = parseFloat(computedStyle.paddingBottom);

            const availableWidth = containerWidth - paddingLeft - paddingRight - offsetX;
            const availableHeight = containerHeight - paddingTop - paddingBottom - offsetY;

            let scale = availableHeight / contentHeight;

            // Width has to be adjusted so that text is always full width
            if (scale < 1 || contentWidth > availableWidth) {
                element.style.transform = `scale(${scale})`;
                element.style.width = `${availableWidth / scale}px`;
                // Force refresh
                document.body.offsetHeight;
                element.classList.add("auto-scaled")
                element.classList.add("s" + (scale*10).toFixed(0))
            } else {
                element.classList.remove("auto-scaled")
                return;
            }
            
            // console.log(`Performed auto scale Scale=${scale.toFixed(2)}, scrollHeight=${(element.scrollHeight * scale).toFixed(2)}, containerHeight=${containerHeight.toFixed(2)}`);

            // If somehow after resizing element significantly smaller than container
            // resizes element by stepping through every scale value
            if (element.scrollHeight * scale < 0.85 * containerHeight) {
                step = 0.05 * (1 - scale)
                scale = 1;
                while (element.scrollHeight * scale >= containerHeight) {
                    scale -= step;
                    element.style.transform = `scale(${scale})`;
                    element.style.width = `${availableWidth / scale}px`;
                    // force dom size to be recalculated
                    document.body.offsetHeight;
                    // console.log(`Scale=${scale.toFixed(2)}, scrollHeight=${(element.scrollHeight * scale).toFixed(2)}, containerHeight=${containerHeight.toFixed(2)}`);
                }
            }
        
        });
    }

    autoScale();

    // update
    window.addEventListener('resize', autoScale);
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('load', autoScale);
    });
    setInterval(autoScale, 1000);
    window.triggerAutoScale = autoScale;
});


// Presentation mode
let isPresentationMode = false;
let currentSlide = 0;
const slides = document.querySelectorAll('.slide-container');

function togglePresentationMode() {
    isPresentationMode = !isPresentationMode;
    if (isPresentationMode) {
        enterPresentationMode();
    } else {
        exitPresentationMode();
    }
}

function enterPresentationMode() {
    document.body.classList.add('presentation-mode');
    // document.body.requestFullscreen().catch(err => console.log(err));
    showSlide(currentSlide);
    document.addEventListener('keydown', handleKeydown);
    fullscreenCheck();
}

function exitPresentationMode() {
    document.exitFullscreen().catch(err => console.log(err));
    document.body.classList.remove('presentation-mode');
    slides.forEach(slide => slide.classList.remove('active'));
    document.removeEventListener('keydown', handleKeydown);
    fullscreenCheck();
}

function handleKeydown(event) {
    switch (event.key) {
        case 'ArrowRight':
        case 'ArrowDown':
            showSlide(currentSlide + 1);
            break;
        case 'ArrowLeft':
        case 'ArrowUp':
            showSlide(currentSlide - 1);
            break;
        case 'Escape':
            togglePresentationMode();
            break;
    }
}

function showSlide(index) {
    if (index < 0) {
        return;
    }
    if (currentSlide < slides.length) {
        slides[currentSlide].classList.remove('active');
    }
    if (index >= slides.length) {
        currentSlide = slides.length;
    } else {
        currentSlide = index
        slides[currentSlide].classList.add('active');
        window.triggerAutoScale();
    }
}

function scaleToFullScreen(element) {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var originalWidth = 720; 
    var originalHeight = 405;

    var scaleX = windowWidth / originalWidth;
    var scaleY = windowHeight / originalHeight;
    var scale = Math.min(scaleX, scaleY);

    element.style.transform = 'scale(' + scale + ')';
    element.style.transformOrigin = 'center';
}

function scaleTo1(element) {
    element.style.transform = null;
    element.style.transformOrigin = null;
}

function fullscreenCheck() {
    if (isPresentationMode) {
        slides.forEach(slide => scaleToFullScreen(slide));
    } else {
        slides.forEach(slide => scaleTo1(slide));
    }
}

window.addEventListener('resize', fullscreenCheck);