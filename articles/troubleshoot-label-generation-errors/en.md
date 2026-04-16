# Troubleshoot Label Generation Errors

## What you'll learn

This guide helps you fix common problems when generating shipping labels on Jamble. If a label fails to generate or something looks wrong, follow the steps here.

## Before you start

You need:
- An approved seller account on Jamble
- A sale waiting for a shipping label

## Common errors and how to fix them

### Error: Label fails to generate

**What it looks like:** You tap the button to generate a label and nothing happens, or you get an error message.

**Common causes and fixes:**

1. **Missing shipping address**
   - Go to **Settings > Shipping Preferences** and make sure your shipping address is complete
   - Your CEP, street, number, city, and state must all be filled in
   - Try updating your CEP — the app auto-fills your address from the postal code

2. **Invalid CEP (postal code)**
   - Make sure your CEP is a valid 8-digit Brazilian postal code
   - If you recently moved, update your address with the correct CEP
   - Some remote CEPs may not be supported by certain Correios services

3. **Buyer address issue**
   - If the buyer's address is incomplete or invalid, the label can't be generated
   - Contact support — they can reach out to the buyer to fix the address

4. **Shipping profile mismatch**
   - If the product's shipping profile doesn't match a valid Correios service for the route (origin → destination), the label may fail
   - Check if the shipping profile assigned to the product is appropriate for its actual size and weight

5. **Temporary service issue**
   - The label system uses an external service (Melhor Envio) to generate Correios labels. If this service is temporarily unavailable, label generation will fail
   - Wait a few minutes and try again. If it persists after 30 minutes, contact support

### Error: Label generated but looks wrong

**What it looks like:** The label PDF opens but the information doesn't look right.

**What to check:**

1. **Wrong sender address** — Your shipping address on the label should match your address in Settings. If it doesn't, update your address in **Settings > Shipping Preferences** before generating new labels
2. **Wrong label format** — If the PDF size doesn't match your printer, change your label format in **Settings > Shipping Preferences** (Half Page, Full Page, or Thermal 4x6)
3. **Wrong items listed** — If the content declaration lists wrong items, this may be a bundling issue. Check if the right products are grouped in the correct bundle

### Error: Can't print or share the label

**What it looks like:** The label opens but the Print button doesn't work or the share sheet doesn't appear.

**What to try:**

1. **Check your internet connection** — The label PDF needs to download. A slow or unstable connection can prevent it from loading
2. **Wait for the PDF to fully load** — The label viewer shows a preview. Make sure the full PDF has loaded before tapping Print
3. **Try again** — Close the label screen and reopen it. The PDF may need to re-download
4. **Save and print from another device** — Use the share menu to send the PDF to yourself via email or save it to Files, then print from a computer

## When to contact support

Contact support if:
- The label keeps failing after multiple attempts and you've verified your address
- The buyer's address seems to be the problem and you can't fix it yourself
- A label was generated with wrong information and you need it replaced
- You've been charged for a label that couldn't be used
- The label generation service has been down for more than an hour

## Important tips

- **Check your address first.** The most common cause of label errors is an incomplete or incorrect shipping address. Verify your CEP, street, and number before anything else
- **Don't generate multiple labels for the same bundle.** If a label fails, troubleshoot the issue before trying again. Generating duplicate labels can cause confusion
- **Keep your app updated.** Label generation improvements are released regularly. Make sure you're running the latest version of the Jamble app
- **Screenshot the error.** If you get an error message, take a screenshot before contacting support. It helps them diagnose the problem faster

## Common questions

**I was charged for a label but it didn't generate properly. Will I get a refund?**
Contact support. If the label was purchased but couldn't be used, they can process a refund for the label cost.

**Can I generate a label from a computer?**
Currently, labels are generated from the Jamble mobile app only. You can export the PDF and print it from any device.

**The label service is down. What should I do?**
Wait and try again later. If it's been more than an hour, contact support. In the meantime, you can generate your own Correios label externally and add the tracking number to the order manually.

**My CEP isn't recognized. What do I do?**
Double-check that you're entering a valid 8-digit CEP. If your area is very new or remote, the CEP may not be in the database yet. Contact support for assistance.

## Need help?

Contact us through the app chat or email support@jambleapp.com.
