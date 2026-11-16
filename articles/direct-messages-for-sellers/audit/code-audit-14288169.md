# Code audit, intercom_id=14288169 (direct-messages-for-sellers)

Checked on 2026-11-13 against released production only:

- iOS: Jamble-iOS tag `5.11` (commit a8acfe38e, release/5.11 merge), paths relative to `Jamble/`
- Android: Jamble-Android tag `v5.11.0`
- Backend: `jamble_backend` `origin/main` (5a4187177, 2026-11-12)

## Files read

| Path | Used for |
|---|---|
| `ACTIVITY/ActivityList/View/ActivityListViewController.swift` | Title "Activity", search bar item (`icon-search`, line 58), search placeholder, bubble filter options (height 36, margin 14, spacing 8) |
| `ACTIVITY/ActivityList/Models/ActivityType.swift` | Six filters: all, messages, unread, purchases, sales, archived |
| `ACTIVITY/ActivityPage/ViewModels/ActivityViewModel.swift` | Filter predicates (lines 119, 129, 132): Messages = no transaction, Sales = seller and transaction, Archived = archived_user_ids |
| `ACTIVITY/ActivityPage/Views/ActivityViewController.swift` | Long press context menu: Archive / Unarchive (lines 225-253) |
| `ACTIVITY/ActivityPage/Views/Components/GroupMessageCell.swift` | Row layout and unread state (seenView 8x8 brand dot, customGrey background, brand date) |
| `MESSAGE/UI/MessageViewController.swift` | Composer (`icon-gallery` button, `message_send`), `selectionLimit = 6` (line 763), long press sheet Copy / Delete this message (own messages only) |
| `MESSAGE/ViewModel/MessageViewModel.swift` | `maxCharacterLimit = 500` (line 48), invisible messages removed from thread (line 580), status row on last own message (lines 711-722) |
| `MESSAGE/UI/Views/MessageStatusRowView.swift` | Time + `check-icon` (sent) or `icon-double-check` brand (read) |
| `MESSAGE/UI/Headers/MessageProductHeader.swift` | Product card at the top of product threads |
| `PROFILE/Views/ProfileHeaderViewController.swift` | Follow + Message buttons on someone else's profile (lines 313-345, 839-841) |
| `PRODUCT/Views/SwiftUI/Components/ProductProfileSection.swift` | Product page chat button, hidden for show products |
| `RESOURCES/Localizable.xcstrings` | Labels below |
| Android `features/activity/.../ActivityType.kt`, `SwipeToArchiveRow.kt`, `values-pt/strings.xml` | Six filters, swipe to archive, pt labels |
| Android `features/messaging/.../MessageInput.kt`, `MessageBubbles.kt`, `values-pt/strings.xml` | 10 photos, Tirar foto / Importar foto, long press, Excluir mensagem, 500-char error, read status |
| Android `features/profile/.../ProfileActions.kt`, `features/product/.../ProductSellerSection.kt` | Follow + Message pair, product page Mensagem |
| jamble_backend `src/services/message_service.py` | send_message (thread creation, membership, moderation, block), perform_can_send_message_checks (lines 1194-1243), send_new_message_notification (lines 1493-1560), attach_group_message_to_transaction (lines 1982-2057) |
| jamble_backend `src/services/purchase_intent_service.py` | get_group_message_for_new_offer (line 3060) |
| jamble_backend `src/schemas/transaction.py` | attach_group_message on created and confirmed (lines 236-237) |
| jamble_backend `src/schemas/product_options.py` | message_seller only when viewer is not owner and product has no show_id (line 57) |
| jamble_backend `src/schemas/user_options.py` | Profile sheet Block / Unblock (line 229) |
| jamble_backend `src/services/notification_service.py` | Atividade > Mensagens toggle (line 3953) |
| jamble_backend `src/enums/error_codes.py` | Public moderation errors (content_privacy, content_off_platform, message_content_invalid) |

## xcstrings keys pulled (verbatim)

| Key | en | pt-BR |
|---|---|---|
| `Activity` | Activity | Atividade |
| `Activity Tab All` | All | Todos |
| `Activity Tab Messages` | Messages | Mensagens |
| `Activity Tab Unread` | Unread | Não lido |
| `Purchases` | Purchases | Compras |
| `Sales` | Sales | Vendas |
| `Activity Tab Archived` | Archived | Concluído |
| `Archive` / `Unarchive` | Archive / Unarchive | Arquivar / Desarquivar |
| `Message` | Message | Mensagem |
| `Follow` | Follow | Seguir |
| `Delete this message` | Delete this message | Excluir esta mensagem |
| `Copy message text` | Copy message text | Copiar o texto da mensagem |
| `You: %@` | You: %@ | Você: %@ |
| `Name, product, order no. or message` | (verbatim) | Nome, produto, nº do pedido ou mensagem |
| `Character limit reached(%lld/%lld characters).` | (verbatim) | Limite de caracteres atingido (%lld/%lld caracteres). |

Android pt (v5.11.0): Todos, Mensagens, Não lidas, Compras, Vendas, Arquivadas; Arquivar / Desarquivar; Excluir mensagem; Tirar foto / Importar foto.

## Article claim, source, verdict

| Article claim | Source | Verdict |
|---|---|---|
| Conversations live in the Activity tab | `ActivityListViewController.swift` title `Activity`; Android ActivityListScreen | MATCH |
| Six filters Todos, Mensagens, Não lido, Compras, Vendas, Arquivadas; iPhone shows the archived filter as Concluído | `ActivityType.swift` + xcstrings (`Activity Tab Archived` pt = Concluído); Android `activity_type_tab_archived` = Arquivadas | MATCH (old article listed 5 filters, missed Mensagens, and called the last one Arquivados) |
| Mensagens = conversations not about an order (questions, offers) | `ActivityViewModel.swift:119` `transaction_id == nil` | MATCH |
| Vendas = conversations about orders you sold | `ActivityViewModel.swift:129` `seller_id == me && transaction_id != nil` | MATCH (old article said Vendas held buyer questions too; it only holds threads with an order) |
| Search by name, product, order number or message from the Activity screen | iOS search bar item + placeholder key; Android `MessageSearchScreen`, `ic_search`; backend `search_group_messages_route` on main | MATCH (new) |
| Plain DM opens from Message next to Follow on a profile | `ProfileHeaderViewController.swift:839-841`; Android `ProfileActions.kt` | MATCH |
| Product thread shows the product at the top; created by a message from a shop product or by an offer | `MessageViewModel.swift` product section, `MessageProductHeader.swift`; backend `product_options.py:57`, `purchase_intent_service.py:3060` | MATCH (old article said only offers create it) |
| Every sale gets an order thread; a shop sale reuses the existing product thread | backend `transaction.py:236-237`, `message_service.py:1982-2057` (find only when no show_id) | MATCH |
| Order thread shows action buttons depending on the order stage | iOS `TransactionActionView` driven by server `TransactionStatusInfosV2` actions | MATCH (wording kept general; old "confirm orders" claim removed) |
| Existing conversation opens, else a new one is created on the first message | `ProfileHeaderViewModel.messageProfile` find_group_message; backend send_message creates the group | MATCH |
| Automatic threads: shop product message, offer, purchase | see the three rows above | MATCH (old bullet "someone contacts you through your profile" removed: not automatic) |
| Text up to 500 characters | iOS `maxCharacterLimit = 500`; Android `character_limit_reached` (/500) | MATCH |
| Photo icon next to the text field; iPhone 6 photos from gallery; Android 10 photos, gallery or camera | iOS `icon-gallery` + `selectionLimit = 6` (images and live photos only); Android `MAX_PICTURES_PER_SEND = 10`, Tirar foto / Importar foto | MATCH (old article said "camera icon" on both) |
| Only text and photos, no audio, video or files | iOS PHPicker filter images + live photos; composer has no other attachment; Android same | MATCH ("links with previews" claim dropped, not verified) |
| Unread: number on the Activity tab, grey background, purple dot | iOS `refreshTabBarActivityLabel`, `GroupMessageCell.swift:244-247`; Android `UnreadConversationsWatcher` | MATCH |
| Archive: long press on iPhone, swipe left on Android; Desarquivar from the archived filter | `ActivityViewController.swift:225-253`; Android `SwipeToArchiveRow.kt` | MATCH (old article said long press on both) |
| Delete: long press own message, delete option; message is removed from the conversation | iOS `didLongPress` delete only if sender; `removeDeletedMessage` sets `is_visible=false`, thread drops it (line 580); Android `delete_message` + "Esta mensagem será removida da conversa." | MATCH (old article said the other person sees "Mensagem cancelada": wrong) |
| Read icon next to the time under your last message | `MessageStatusRowView.swift` read = `icon-double-check`; Android `ic_is_read` | MATCH (new detail) |
| Push for each new private message with sender name, text or "Te enviou uma foto", product image | backend `send_new_message_notification` (pt "Te enviou uma foto", en "Just sent you a photo") | MATCH (old pt said "Acabou de te enviar uma foto": wrong) |
| In-app notification option Mensagens | backend `notification_service.py:3953` (Atividade > Mensagens) | MATCH |
| Personal data and off-platform invitations blocked before delivery; offensive messages blocked | backend `send_message` refuses these with user-visible errors | MATCH (no thresholds or detection logic stated) |
| Blocked users cannot message you; Block from the profile options menu | backend `perform_can_send_message_checks` `block_exists`; `user_options.py:229` profile sheet Block | MATCH |
| No bulk messaging | no broadcast endpoint in `routers/message.py` | MATCH |
| Removed: "a few messages per conversation every few seconds" rate-limit FAQ | the described limit does not apply to DMs | REMOVED (wrong for DMs, and limits are internal) |

Zero open MISMATCH.

## Layout proof table (activity-tabs)

| UI element | iOS source | Parent container | Order | Alignment | Size / style | HTML selector |
|---|---|---|---|---|---|---|
| Title "Atividade" | `ActivityListViewController.swift:49-55, 256-259` | view safe area | first | leading 12 | height 50, `.title(.S)` 24 medium, tracking -0.24 | `.title` |
| Filter pills | `ActivityListViewController.swift:17-37`, `BubblePageFilterCell.swift:56-115`, `PageControllerOptions.swift:98-100` | pageContainer | below title (+10) | horizontal scroll, spacing 8 | height 36, radius 18, margin 14, 16 semibold, selected black/white, unselected white with #DADDE3 border | `.filters .pill`, `.pill.on` |
| Row container | `GroupMessageCell.swift:96-101, 143-146` | collection cell | list | inset 8 horizontal, 4 vertical | radius 12, white or #F0F1F5 when unread | `.row`, `.row.unread` |
| Avatar | `GroupMessageCell.swift:14-23, 150-155` | row | leading | leading 8, top/bottom 8 | 64x64 radius 12 (user photo, shown as neutral swatch) | `.avatar` |
| Name | `GroupMessageCell.swift:25-33` | info container | top | leading avatar+8 | 14 semibold black | `.name` |
| Preview | `GroupMessageCell.swift:35-41, 238-242` | info container | below name +5 | same | 14 medium twitterGrey (#566371) | `.preview` |
| Date | `GroupMessageCell.swift:43-53, 158-163, 247` | row | trailing | trailing 8, centerY top+20, width 60 | 14 semibold, #A4A8AC or brand when unread | `.date` |
| Unread dot | `GroupMessageCell.swift:56-63, 165-170` | row | trailing | trailing 8, centerY row | 8x8 radius 4 brand | `.dot` |

Cropped on purpose: navigation bar items (search, help) and the tab bar. The Patron title font is replaced by the system font (sub-pixel divergence accepted by process/10).

## Visual fidelity

| Mockup | Compared against | Result |
|---|---|---|
| `direct-messages-for-sellers__activity-tabs__pt-br__v3.png` | iOS 5.11 code (layout proof table above), no simulator run | code-only |
| `direct-messages-for-sellers__activity-tabs__en__v3.png` | same | code-only |

Dropped screens: `dm-product-card`, `product-message-thread`, `user-profile-header`. Their HTML sources were placeholders (a purple square with a dot as product image, an empty body, a bare "@username / 1.2k followers" card) that do not match `MessageProductHeader.swift` or `ProfileHeaderViewController.swift`, and the PNGs were never rendered. The product header also shows platform-specific button labels (iOS "Editar listagem" / "Contrapor"), so it was not rebuilt.
