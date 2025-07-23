STRATEGIES = {
    'MSC': {
        'url': 'https://www.msc.com/en/track-a-shipment',
        'input_locators': [
            ('id', 'trackingNumber'),
            ('xpath', "//input[@placeholder='Enter a Container/Bill of Lading Number']"),
            ('name', 'trackingNumber'),
            ('xpath', "//input[contains(@placeholder, 'Container')]"),
            ('xpath', "//input[contains(@placeholder, 'Bill of Lading')]"),
        ],
        'result_indicators': [
            ('class_name', 'msc-flow-tracking__wrapper'),
        ],
        'eta_patterns': [
            r'Price Calculation Date\*[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})',
            r'Price Calculation Date\s*\*?\s*[:\-]?\s*([0-9]{2}/[0-9]{2}/[0-9]{4})',
            r'POD ETA[:\s]*(\d{2}/\d{2}/\d{4})',
            r'Estimated Time of Arrival[:\s]*(\d{2}/\d{2}/\d{4})',
            r'ETA[:\s]*(\d{2}/\d{2}/\d{4})',
        ]
    },
}