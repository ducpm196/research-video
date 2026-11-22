decide = lambda votes: 'COMMIT' if all(v == 'YES' for v in votes) else 'ABORT'
state, coord_up = 'PREPARED', False
print(f'all_yes_commit={int(decide(["YES","YES"]) == "COMMIT")}')
print(f'one_no_abort={int(decide(["YES","NO"]) == "ABORT")}')
print(f'prepared_blocked_on_coord_loss={int(state == "PREPARED" and not coord_up)}')
