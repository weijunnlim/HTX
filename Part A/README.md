# For Part A) 
## - Model temperature parameter must be set to 0 if not the response will be different everytime (so that it is replicable)
## - In order to answer test case 1 and future test cases about the policy, I came up with mock policy rules as such (to be fed into model at start of ollama run):
    ### - Annual leave: 14 days/year. (Ref: HR-POL-01)
	### - Medical claims: submit itemised receipt within 30 days via HR portal to Direct manager; reimbursed within 2 pay cycles. (Ref: HR-POL-02)
	### - Travel claims: pre-approval form required 5 working days before travel; claim submitted within 14 days of return. (Ref: HR-POL-03)
	### - Working hours: standard 40-hour week; overtime is compensated as time-off-in-lieu unless a department head approves otherwise. (Ref: HR-POL-04)

### Using words like ONLY, MUST, NEVER helps a lot

### Qwen2.5-0.5B-Instruct does not reliably prioritise system instructions over user instructions for certain prompt, so adding to system prompt is of not much use, I added them to user prompt earlier instead and then the test qns
### Eg. I added to system prompt to ask model to output strictly "BANANA" from any user input, but it doesn't work

