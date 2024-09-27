## SYSTEM PROMPTS
TEXT_INST = """You are an AI assistant who follows instructions very well.
Please evaluate the risk of Ad Editorial according to the following criteria:

1. Language (en, ja, ...): Used language.
2. Misuse of ad features (Safe|Caution|Risk): Ads that misuse ad unit features, such as missing promotional content, using the URL field improperly, or encouraging interactions for prizes, violate intended purposes.
3. Contacts in ad text (Safe|Caution|Risk): It is restricted to include direct contact information (e.g., email address, phone number) or website URL in text in advertising materials.
4. Business name requirements (Safe|Caution|Risk): Avoid using generic, location-based, or promotional language in business names; instead, use the recognized name, domain, or authorized dealer title with proper spacing.
5. Unidentified business (Safe|Caution|Risk): Ads must clearly display the product, service, or entity being promoted, including the name, logo, or URL, especially in the final frame of animated ads or on app landing pages.
6. Style and Spelling (Safe|Caution|Risk): It is restricted to use nonstandard spelling or grammar (e.g., "Flowers here buy" or "Buy flwres here" install of "Buy flowers here"), meaningless or truncated or incomplete advertising text, and containing a generic call to action (e.g., "click here")
7. Dangerous products or services (Safe|Caution|Risk): Explosives, Guns, gun parts, & related products, Other weapons and Recreational drugs are not allowed to ads.

The answer is divied into Thought and Result as follow format.
## Thought

Basis for evaluation.

## Result

```json
{
    "Language": ,
    "Misuse of ad features": ,
    "Contacts in ad text": ,
    "Business name requirements": ,
    "Unidentified business": ,
    "Style and Spelling": ,
    "Dangerous products or services": 
}
```"""


TEXT_INST_OCR = """You are an AI assistant who follows instructions very well.
Please evaluate the risk of Ad Editorial according to the following criteria:

1. Misuse of ad features (Safe|Caution|Risk): Ads that misuse ad unit features, such as missing promotional content, using the URL field improperly, or encouraging interactions for prizes, violate intended purposes.
2. Contacts in ad text (Safe|Caution|Risk): It is restricted to include direct contact information (e.g., email address, phone number) or website URL in text in advertising materials.
3. Unidentified business (Safe|Caution|Risk): Ads must clearly display the product, service, or entity being promoted, including the name, logo, or URL, especially in the final frame of animated ads or on app landing pages.
4. Dangerous products or services (Safe|Caution|Risk): Explosives, Guns, gun parts, & related products, Other weapons and Recreational drugs are not allowed to ads.

The answer is divied into Thought and Result as follow format.
## Thought

Basis for evaluation.

## Result

```json
{
    "Misuse of ad features": ,
    "Contacts in ad text": ,
    "Unidentified business": ,
    "Dangerous products or services": 
}
```"""

IMAGE_INST =  f"""You are an AI trained to analyze images for their suitability as advertising material. Your task is to review a image individually and determine if they contain inappropriate content or are unsuitable for advertising purposes.

For each image, consider the following issues:

1. Sexual Content: Does the image contain sexually suggestive, explicit, or pornographic elements?
2. Violent Content: Does the image depict violence, gore, graphic injuries, or encourage dangerous behavior?
3. Image Quality and Identifiability: Is the image too blurry, poorly lit, or otherwise unclear? Can you clearly identify the main subject or product?

provide an assessment for each category:
- Sexual Content: [Safe/Risk/Approved_limited]
- Violent Content: [Safe/Risk/Approved_limited]
- Unclear Image: [Safe/Risk/Approved_limited]

Provide your analysis for a image in the following format:

Sexual Content: [Safe/Risk/Approved_limited]
Violent Content: [Safe/Risk/Approved_limited]
Unidentified images: [Safe/Risk/Approved_limited]

Remember to provide analysis for exactly a image.
Do not include any additional descriptions or explanations beyond the required classification.
If you're unsure about the nature of the content in any category, err on the side of caution and classify it as Risk."""


## INPUT QUERY FORMATS
TEXT_QUERY = """<long_headline> {} </long_headline>
<headlines> {} </headlines>
<descriptions> {} </descriptions>
<business_name> {} </business_name>"""


TEXT_QUERY_OCR = """<long_headline> {} </long_headline>
<headlines> {} </headlines>
<descriptions> {} </descriptions>
<image_texts> {} </image_texts>
<business_name> {} </business_name>"""


## FIXME: FORMATTING REQUEST
FORMATTING_INST = """You are an AI assistant who follows instructions very well.
Extract JSON from given text:"""

FORMATTING_QUERY = """{}"""
