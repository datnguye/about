// PDF Download functionality for Resume using html2canvas and jsPDF
document.addEventListener('DOMContentLoaded', function() {
    // Only run on resume page
    const isResumePage = document.querySelector('.resume-container') !== null;
    if (!isResumePage) {
        return;
    }
    
    // Create download button
    function createDownloadButton() {
        const button = document.createElement('button');
        button.className = 'pdf-download-btn';
        button.innerHTML = '<i class="fas fa-download"></i>';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            padding: 0;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 1000;
            font-size: 18px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        button.addEventListener('mouseenter', function() {
            this.style.opacity = '0.8';
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 12px rgba(0,0,0,0.15)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.opacity = '1';
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
        
        button.addEventListener('click', downloadResumePDF);
        
        document.body.appendChild(button);
    }
    
    // Download Resume as PDF with styling preserved
    async function downloadResumePDF() {
        // Show BuyMeACoffee popup
        showBuyMeACoffeePopup();
    }
    
    // Show popup with BuyMeACoffee link
    function showBuyMeACoffeePopup() {
        const button = document.querySelector('.pdf-download-btn');
        const buttonRect = button.getBoundingClientRect();
        
        // Create overlay (lighter, just to capture clicks)
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: transparent;
            z-index: 9998;
        `;
        
        // Create popup positioned near the button
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            bottom: ${window.innerHeight - buttonRect.top + 10}px;
            right: 20px;
            background-color: var(--card);
            color: var(--text);
            padding: 20px;
            border-radius: 10px;
            width: 300px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 9999;
            border: 1px solid var(--border);
        `;
        
        popup.innerHTML = `
            <h4 style="margin-bottom: 10px; color: var(--primary); font-size: 16px;">☕ Support My Work</h4>
            <p style="margin-bottom: 15px; font-size: 14px;">Found your next hire 🎯 OR resume template 📋? Either way, coffee ☕ keeps me updating it! 🚀✨</p>
            <a href="https://buymeacoffee.com/datnguye" target="_blank" style="
                display: inline-block;
                background-color: #FFDD00;
                color: #000;
                padding: 8px 16px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
                margin-bottom: 15px;
                font-size: 14px;
            ">☕ Buy Me a Coffee</a>
            <div style="margin-top: 15px; display: flex; gap: 10px; justify-content: center;">
                <button id="downloadNow" style="
                    background-color: var(--primary);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 13px;
                    flex: 1;
                ">Download Resume</button>
                <button id="cancelDownload" style="
                    background-color: transparent;
                    color: var(--text);
                    border: 1px solid var(--border);
                    padding: 8px 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 13px;
                    flex: 1;
                ">Cancel</button>
            </div>
        `;
        
        overlay.appendChild(popup);
        document.body.appendChild(overlay);
        
        // Event handlers
        document.getElementById('downloadNow').addEventListener('click', () => {
            document.body.removeChild(overlay);
            proceedWithDownload();
        });
        
        document.getElementById('cancelDownload').addEventListener('click', () => {
            document.body.removeChild(overlay);
        });
        
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
            }
        });
    }
    
    // Actual download function
    async function proceedWithDownload() {
        const button = document.querySelector('.pdf-download-btn');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        button.disabled = true;
        
        try {
            // Get all the content we want to include in PDF
            const header = document.querySelector('.container > header') || document.querySelector('header');
            const resumeContainer = document.querySelector('.resume-container');
            
            // Get the current theme colors from CSS variables
            const computedStyle = getComputedStyle(document.documentElement);
            const backgroundColor = computedStyle.getPropertyValue('--background').trim() || 
                                  getComputedStyle(document.body).backgroundColor;
            const textColor = computedStyle.getPropertyValue('--text').trim();
            const cardColor = computedStyle.getPropertyValue('--card').trim();
            
            // Create a temporary container for PDF content
            const pdfContainer = document.createElement('div');
            pdfContainer.className = 'pdf-export-container';
            pdfContainer.style.cssText = `
                position: absolute;
                left: -9999px;
                top: 0;
                width: 1200px;
                background: ${backgroundColor};
                color: ${textColor};
                padding: 60px;
                font-family: inherit;
                min-height: 100vh;
            `;
            
            // Copy all CSS custom properties to the container
            const allStyles = computedStyle.cssText;
            if (allStyles) {
                pdfContainer.style.cssText += allStyles;
            } else {
                // Fallback: manually copy CSS variables
                for (let i = 0; i < computedStyle.length; i++) {
                    const propName = computedStyle[i];
                    if (propName.startsWith('--')) {
                        pdfContainer.style.setProperty(propName, computedStyle.getPropertyValue(propName));
                    }
                }
            }
            
            // Clone header if it exists and is outside resume container
            if (header && !resumeContainer.contains(header)) {
                const headerClone = header.cloneNode(true);
                // Remove navigation if present
                const nav = headerClone.querySelector('nav');
                if (nav) nav.remove();
                pdfContainer.appendChild(headerClone);
            }
            
            // Clone resume content
            const resumeClone = resumeContainer.cloneNode(true);
            
            // Clone canvas elements with their content
            const originalCanvases = resumeContainer.querySelectorAll('canvas');
            const clonedCanvases = resumeClone.querySelectorAll('canvas');
            
            originalCanvases.forEach((originalCanvas, index) => {
                if (clonedCanvases[index]) {
                    const clonedCanvas = clonedCanvases[index];
                    const context = clonedCanvas.getContext('2d');
                    clonedCanvas.width = originalCanvas.width;
                    clonedCanvas.height = originalCanvas.height;
                    context.drawImage(originalCanvas, 0, 0);
                }
            });
            
            // Remove any download buttons from the clone
            resumeClone.querySelectorAll('.pdf-download-btn').forEach(btn => btn.remove());
            
            // Expand all details/summary elements
            resumeClone.querySelectorAll('details').forEach(detail => {
                detail.setAttribute('open', 'true');
            });
            
            // Expand the "Show More" experience section
            const olderExperience = resumeClone.querySelector('#olderExperience');
            if (olderExperience) {
                olderExperience.style.maxHeight = 'none';
                olderExperience.style.overflow = 'visible';
            }
            
            // Hide the toggle button
            const toggleButton = resumeClone.querySelector('#toggleExperience');
            if (toggleButton) {
                toggleButton.style.display = 'none';
            }
            
            // Expand any other collapsible sections
            resumeClone.querySelectorAll('[style*="max-height"]').forEach(el => {
                el.style.maxHeight = 'none';
                el.style.overflow = 'visible';
            });
            
            // Remove any floating background elements
            resumeClone.querySelectorAll('.floating').forEach(el => el.remove());
            
            // Apply body classes to container for proper theme styling
            pdfContainer.className = document.body.className + ' pdf-export-container';
            
            pdfContainer.appendChild(resumeClone);
            
            // Show all hidden phone numbers in the PDF container
            const allPhoneElements = pdfContainer.querySelectorAll('.phone-hidden');
            allPhoneElements.forEach(el => {
                el.classList.remove('phone-hidden');
                el.style.display = 'flex'; // Ensure it's visible
            });
            
            // Add footer with website URL
            const footer = document.createElement('div');
            footer.style.cssText = `
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid ${getComputedStyle(document.documentElement).getPropertyValue('--border').trim()};
                text-align: center;
                font-size: 12px;
                color: ${textColor};
                opacity: 0.7;
            `;
            footer.innerHTML = `
                <p>View online at: <a href="${window.location.origin}" style="color: var(--primary); text-decoration: none;">${window.location.hostname}</a></p>
                <p style="margin-top: 5px;">Generated on ${new Date().toLocaleDateString()}</p>
            `;
            pdfContainer.appendChild(footer);
            
            document.body.appendChild(pdfContainer);
            
            // Wait a moment for DOM to update
            await new Promise(resolve => setTimeout(resolve, 50));
            
            // Add extra spacing before Languages section to push it to next page
            const allSections = pdfContainer.querySelectorAll('.resume-section');
            allSections.forEach(section => {
                const heading = section.querySelector('h2');
                if (heading && heading.textContent.includes('Languages')) {
                    // Add a margin to push it to the next page
                    section.style.marginTop = '50px';
                    // Add a spacer div before the section
                    const spacer = document.createElement('div');
                    spacer.style.height = '50px';
                    section.parentNode.insertBefore(spacer, section);
                }
            });
            
            // Remove "Current" text from experience items
            pdfContainer.querySelectorAll('*').forEach(element => {
                if (element.textContent === 'Current' && element.tagName === 'SPAN') {
                    element.remove();
                }
            });
            
            // Now apply style fixes after DOM is ready
            // This selector covers all elements with colored backgrounds (red, green, etc.)
            pdfContainer.querySelectorAll('[class*="bg-"][class*="opacity"], [class*="bg-green"], [class*="bg-\\[var\\(--primary\\)\\]"], [class*="bg-\\[var\\(--secondary\\)\\]"], [class*="bg-\\[var\\(--accent\\)\\]"]').forEach(tag => {
                // Only apply to small badges/tags, not large sections
                if (tag.tagName === 'SPAN' || tag.classList.contains('px-2') || tag.classList.contains('py-1') || tag.classList.contains('rounded')) {
                    // Force inline styles with !important
                    tag.setAttribute('style', `
                        background-color: transparent !important;
                        border: none !important;
                        padding: 0 !important;
                        margin: 0 4px 0 0 !important;
                        display: inline !important;
                        color: #666 !important;
                        font-style: italic !important;
                    `);
                }
            });
            
            // Use html2canvas to capture the content
            const canvas = await html2canvas(pdfContainer, {
                scale: 2, // Higher quality
                useCORS: true,
                logging: false,
                backgroundColor: backgroundColor,
                windowWidth: 1200,
                windowHeight: pdfContainer.scrollHeight
            });
            
            // Remove temporary container
            document.body.removeChild(pdfContainer);
            
            // Calculate PDF dimensions - full page with no margins
            const imgWidth = 210; // A4 width in mm
            const pageHeight = 297; // A4 height in mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            let heightLeft = imgHeight;
            
            // Initialize jsPDF with no margins
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'mm',
                format: 'a4',
                compress: true
            });
            
            // Set background color for the entire PDF
            pdf.setFillColor(backgroundColor);
            pdf.rect(0, 0, imgWidth, pageHeight, 'F');
            
            let position = 0;
            
            // Add first page - full bleed (no margins)
            pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight, '', 'FAST');
            heightLeft -= pageHeight;
            
            // Add additional pages if needed
            while (heightLeft >= 0) {
                position = heightLeft - imgHeight;
                pdf.addPage();
                // Fill background for each new page
                pdf.setFillColor(backgroundColor);
                pdf.rect(0, 0, imgWidth, pageHeight, 'F');
                pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight, '', 'FAST');
                heightLeft -= pageHeight;
            }
            
            // Save the PDF
            const timestamp = new Date().toISOString().split('T')[0];
            pdf.save(`Resume_DatNguyen_${timestamp}.pdf`);
            
            // Reset button
            button.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
            
        } catch (error) {
            console.error('Error generating PDF:', error);
            button.innerHTML = '<i class="fas fa-times"></i>';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        }
    }
    
    // Initialize download button
    createDownloadButton();
});