import streamlit as st

def load_design():
    # Load CSS
    with open("styles/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Inject JS for cursor tracking and Background Div
    st.markdown("""
    <script>
    document.addEventListener('mousemove', function(e) {
        const x = e.clientX;
        const y = e.clientY;
        document.body.style.setProperty('--mouse-x', x + 'px');
        document.body.style.setProperty('--mouse-y', y + 'px');
        
        // Parallax for shapes
        const shapes = document.querySelectorAll('.floating-shape');
        shapes.forEach(shape => {
            const speed = shape.getAttribute('data-speed');
            const xOffset = (window.innerWidth - x * speed) / 100;
            const yOffset = (window.innerHeight - y * speed) / 100;
            shape.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
        });
    });
    </script>
    
    <div class="interactive-background"></div>
    
    <!-- Geometric Patterns -->
    <div class="background-patterns">
        <div class="floating-shape shape-circle" data-speed="5"></div>
        <div class="floating-shape shape-circle-2" data-speed="-2"></div>
        <div class="floating-shape shape-line" data-speed="3"></div>
        <div class="floating-shape shape-square" data-speed="4"></div>
        <div class="grid-overlay"></div>
    </div>
    """, unsafe_allow_html=True)
