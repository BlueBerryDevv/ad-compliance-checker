# ad-compliance-checker

This repository contains the code for an AI-powered advertisement content validator using Gemma. The tool is designed to review ad materials for compliance with Google's advertising policies and provide guidance on potential violations.

<img src="./static/image/check_bear.jpeg">

## Features


1. Text Analysis
   - Detect excessive use of special characters
   - Identify repetitive content
   - Flag click-bait phrases

2. Image Analysis
   - Detect misuse of play buttons or sound icons
   - Identify potentially harmful or inappropriate images

3. Phone Number Verification
   - Check for presence and format of phone numbers in ad copy

4. Video Quality Assessment
   - Analyze video content for quality and compliance

5. Harmful Product/Service Detection
   - Identify advertisements for potentially dangerous products or services

6. Healthcare and Medication Ad Review
   - Special checks for ads related to healthcare and pharmaceutical products

## Installation

```bash
git clone https://github.com/your-username/gemma-ad-compliance-checker.git
cd gemma-ad-compliance-checker
pip install -r requirements.txt
```
## Configuration
Adjust the config.yaml file to customize the validation rules and thresholds.


## License

Copyright (c) 2024 A1 Media Group. All rights reserved.

This software and associated documentation files (the "Software") are proprietary and confidential. 
Unauthorized copying, transfer or use of the Software, via any medium is strictly prohibited without the express written permission of [회사명].

The Software incorporates Gemma, which is licensed under the Apache License 2.0.

## Acknowledgments

Google for providing the Gemma model
The open-source community for various tools and libraries used in this project
