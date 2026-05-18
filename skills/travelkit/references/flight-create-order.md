# flight-create-order ref

## flight_create_order

价格验证通过且用户确认继续后，收集乘客信息；下单前再次明确确认，创建订单但不自动支付。

### When to use

Use after `flight_verify_solution` succeeds and the user says they want to continue booking. Do not collect ID, passport, phone, or email before this point.

### Passenger collection prompt

Before collecting details, briefly state the document type needed. For Hong Kong/Macau/Taiwan routes or unclear route types, ask which valid travel document the passenger will use. Use natural Chinese + Markdown bullets, not code blocks or blank forms.

Domestic mainland flights default to the ID-card Chinese-name template. Do not ask for pinyin or English surname/given names for domestic ID-card passengers. Use the passport English-name template only for international routes or passport/English-name document scenarios.

When using a fixed prompt below, output it verbatim: do not rewrite it, compress it into one line, merge fields, remove fields, or change field order.
Do not add examples, placeholders, date formats, or sample values to the fixed prompt. In particular, the birthday field must be exactly `- 出生日期`; never append any date example or format hint.
Do not narrow passenger type choices based on the searched passenger count. The passenger type field must always be exactly `- 乘客类型：成人 / 儿童 / 婴儿`, even when the current request is for one adult.

**Domestic fixed prompt - must output verbatim**:

> 这趟是国内航班，后续需要乘机人身份证信息。请把下面信息发我，我再帮你创建订单，但不会自动支付：
> 中文姓名我会按证件姓名识别姓、名；如果复姓或拆分不确定，我再单独确认。

- 乘机人姓名
- 出生日期
- 性别
- 乘客类型：成人 / 儿童 / 婴儿
- 国籍
- 证件类型：中国居民身份证 或 其他
- 身份证号码
- 乘机人手机号
- 乘机人邮箱

**International fixed prompt - must output verbatim**:

> 这趟是国际航班，后续需要乘机人护照信息。请把下面信息发我，我再帮你创建订单，但不会自动支付：
> 护照英文姓和英文名需要与护照完全一致。

- 护照英文姓 / surname
- 护照英文名 / given names
- 出生日期
- 性别
- 乘客类型：成人 / 儿童 / 婴儿
- 国籍
- 护照号码
- 护照有效期
- 乘机人手机号
- 乘机人邮箱

Every passenger must have phone, email, document type, and document number. ID card, Mainland Travel Permit, and Taiwan Travel Permit names use Chinese as shown on the document; passports use the passport English name. For ID-card passengers, ask users for one Chinese full name and split internally; ask only when compound surname, ethnic/minority name, English name, very long name, or rare characters make the split uncertain.

If contact name/phone is absent, default to the first passenger's name and phone, mention this briefly before order creation, and do not collect contact email.

### Confirmation before creation

Before `flight_create_order`, summarize flight/route, departure and arrival time, passengers, contact info including defaults, final price, and important tool-returned notices. Final price follows the shared amount rule: total price = fare + tax.

The amount line in the pre-creation confirmation summary must use this single-line format:

> 金额：¥{总价}（票面价 ¥{票面价} + 税价 ¥{税价}）

Do not use an equation-style amount line or split the pre-creation confirmation amount into separate fare/tax/total lines.

Ask:
> 确认后我会为你创建订单，但不会自动支付。是否确认创建？

Call `flight_create_order` only after explicit confirmation. Use the verified `orderKey`; set all required internal confirmation fields in the tool call without mentioning production or technical flags to the user.

### After creation

After success, call `flight_order_detail` when useful and show the fixed order information template from `output-rules`. The user-facing order summary must include order info, passengers, segments, amount, and next step in that exact template order.

Deadlines must come from explicit tool fields. If missing, use the fixed deadline wording from `output-rules`.

Amount must follow the shared amount rule: total price = fare + tax. Use returned fare and tax fields when available; for multiple passengers or segments, sum fare and tax separately before calculating total price. If the tool returns only total amount without a fare/tax split, use the fixed single amount line from `output-rules` and mark the missing split values as "未返回"; do not invent a split.

If unpaid, prompt payment options without balance payment: domestic uses 微信、支付宝、信用卡、借记卡; international/cross-border can also include Airwallex.

### Errors

On failure, briefly explain and ask only for missing or corrected fields. Name-related errors (`FirstName`, `LastName`, ID-card full name, etc.) mean the document-name format does not meet supplier requirements; do not blame price or inventory. If an abnormal order is unpaid and unticketed, re-verify price before creating a corrected new order.
