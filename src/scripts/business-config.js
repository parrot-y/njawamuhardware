/**
 * Business Config — Single Source of Truth
 * All contact details and helper utilities used across the site.
 */

window.BusinessConfig = {
    phone: '254726822382',
    phoneDisplay: '+254 726 822 382',
    whatsapp: '254726822382',
    email: 'info@njawamuhardware.com',
    businessName: 'NJAWAMU Hardware',
    location: 'MSP PLAZA Room G14, Kirinyaga Road, Nairobi',
    generalInquiryMsg: "Hello NJAWAMU Hardware! 👋 I have a general inquiry about your products.",

    /** Validate WhatsApp number: digits only, 10–15 digits */
    isValidWhatsApp(number) {
        const digits = String(number).replace(/\D/g, '');
        return digits.length >= 10 && digits.length <= 15;
    },

    /** Open WhatsApp with message, or show error if number is invalid */
    openWhatsApp(message) {
        const num = String(this.whatsapp).replace(/\D/g, '');
        if (!this.isValidWhatsApp(num)) {
            this._showError('Unable to connect to WhatsApp. Please call us directly at ' + this.phoneDisplay);
            return false;
        }
        const text = message || this.generalInquiryMsg;
        const url = `https://wa.me/${num}?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
        return true;
    },

    /** Build tel: link */
    telLink() {
        return `tel:+${this.phone}`;
    },

    /** Build mailto: link */
    mailtoLink() {
        return `mailto:${this.email}`;
    },

    /** Build wa.me link (with optional message) */
    whatsappLink(msg) {
        const text = msg || this.generalInquiryMsg;
        return `https://wa.me/${this.whatsapp}?text=${encodeURIComponent(text)}`;
    },

    /** Show a user-facing error toast */
    _showError(msg) {
        // Uses the existing toast system if available, otherwise alert
        if (typeof showToast === 'function') {
            showToast(msg);
        } else {
            alert(msg);
        }
    }
};
