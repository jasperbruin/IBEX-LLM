# Futarchy Phase Instructions

These are the instructions that I use for Futarchy for each phase:

## Phase-Specific Prompts:

### 1. **Market Phase Prompt**:
```plaintext
"Market Phase: Players now see their private signals and the public signals. Use these signals to decide your next trading move.\n\n"
"**Your available balance is {total_balance}. You cannot place a bid or ask that exceeds this amount.**\n\n"
"The signals represent market data, and you should interpret them to determine whether you wish to post a buy (bid) or sell (ask) order.\n\n"
"Market Signals:\n"
"- 'signals': Your private signals, visible only to you\n"
"- 'publicSignal': Signals visible to all players\n"
"Use this data to inform your decision. You are responsible for setting the prices based on these signals.\n\n"
"**You must ensure that the 'price' in your order does not exceed your available balance.**\n\n"
"Expected JSON Output (Post Order):\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"post-order\",\n"
" \"order\": {\n"
" \"price\": your_chosen_price if 1 <= your_chosen_price <= {max_price},\n"
" \"quantity\": 1,\n"
" \"condition\": condition_number,\n"
" \"type\": \"ask\" or \"bid\",\n"
" \"now\": false\n"
" }\n}}"
```

### 2. **Phase 0: Player Ready Prompt**:
```plaintext
"Player is Ready: The game waits until all players declare themselves ready. No action is required.\n\n"
"Expected JSON Output:\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"player-is-ready\"\n}}"
```

### 3. **Phase 2: Declaration Phase Prompt**:
```plaintext
"Declaration Phase: Owners and Developer should declare their expected revenue for the round.\n\n"
"The 'declaration' array should contain three values:\n"
"- Value for the status quo condition (no project)\n"
"- Value for the project development\n"
"- Optional third value, set to 0 (for future use)\n\n"
"Expected JSON Output:\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"declare\",\n"
" \"declaration\": [\n"
" value_for_no_project,\n"
" value_for_project,\n"
" 0\n"
" ]\n}}"
```

### 4. **Phase 3: Speculation Phase Prompt**:
```plaintext
"Speculation Phase: Speculators may challenge declarations by Owners and Developers.\n\n"
"The 'snipe' array should contain two arrays:\n"
"- First array lists owners to challenge for the status quo condition\n"
"- Second array lists owners to challenge for the project development condition\n\n"
"Expected JSON Output:\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"done-speculating\",\n"
" \"snipe\": [\n"
" [owners_to_challenge_no_project],\n"
" [owners_to_challenge_project]\n"
" ]\n}}"
```

### 5. **Phase 7: Final Declaration Prompt**:
```plaintext
"Final Declaration Phase: Owners and Developers submit their final declaration for the winning condition.\n\n"
"Expected JSON Output:\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"declare\",\n"
" \"declaration\": [\n"
" final_value_for_winning_condition\n"
" ]\n}}"
```

### 6. **Phase 8: Final Speculation Phase Prompt**:
```plaintext
"Final Speculation Phase: Speculators can challenge the final declarations.\n\n"
"The 'snipe' array works similarly to Phase 3, where speculators list owners to challenge.\n\n"
"Expected JSON Output:\n{{\n"
" \"gameId\": {self.game_id},\n"
" \"type\": \"done-speculating\",\n"
" \"snipe\": [\n"
" [owners_to_challenge]\n"
" ]\n}}"
```

## Cummalative Context - Included in each, but this is a Market Phase example:

```plaintext
Cumulative Context:

Past Phase Transitions (last 10):
- Phase 1 (Round 5), Phase 2 (Round 5), Phase 3 (Round 5), Phase 4 (Round 5), Phase 5 (Round 5), Phase 6 (Round 5)

Recent Player Actions (last 20):
- Phase transition
- Phase transition
- Declarations Published: Lesser Albatross Lot by Tan - Declarations: [45000, 55000, 0]; Bloody Llama Lot by Blue - Declarations: [10000, 50000, 0]
- Phase transition
- Phase transition
- Market Signals: Signals=[8907, 9812, 0], PublicSignal=[181.5, 346.5, 0], Tax Rate=33
- Phase transition
- Phase transition
- Add Order: ID=1, Sender=2, Price=55000, Type=ask, Condition=0
- Add Order: ID=2, Sender=3, Price=10500, Type=bid, Condition=0
- Add Order: ID=1, Sender=2, Price=55000, Type=ask, Condition=0
- Add Order: ID=2, Sender=3, Price=10500, Type=bid, Condition=0
- Add Order: ID=3, Sender=1, Price=51000, Type=bid, Condition=0
- Add Order: ID=4, Sender=2, Price=53000, Type=bid, Condition=0
- Add Order: ID=5, Sender=3, Price=10000, Type=bid, Condition=0
- Add Order: ID=3, Sender=1, Price=51000, Type=bid, Condition=0
- Add Order: ID=4, Sender=2, Price=53000, Type=bid, Condition=0
- Add Order: ID=5, Sender=3, Price=10000, Type=bid, Condition=0

Recent Declarations (last 5):
- **Lesser Albatross Lot by Tan** - Declarations: [45000, 55000, 0]
- **Bloody Llama Lot by Blue** - Declarations: [10000, 50000, 0]

Recent Market Signals (last 5):
- Signals: [8907, 9812, 0], Tax Rate: 33

- **Player Status:**
- **Total Wallet Balance:** 600000
- **Balance for Condition 0 (Left Market):** 300000
- **Balance for Condition 1 (Right Market):** 300000
- **Shares for Condition 0 (Left Market):** 30
- **Shares for Condition 1 (Right Market):** 30
- **Cash for Sniping Condition 0:** 250000
- **Cash for Sniping Condition 1:** 250000
- **Properties Owned:** Bloody Llama Lot
- **Latest Market Signal:** Signals=[8907, 9812, 0], Tax Rate=33

## Important Instructions:

- When generating your response, ensure that any bid or ask price does not exceed your available wallet balance.
- Your available balance is provided in the 'Player Status' section above.
- Make sure to consider your balance when deciding on the price for bids or asks.
- Do not attempt to place orders that you cannot afford.
```