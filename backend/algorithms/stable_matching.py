def gale_shapley(mpref, wpref, n, F):
    ### returns men's matchings or proposers' matchings i.e. men_matchings[i] is a partner of proposer i
    curr_match_count = 0
    last_rejected_by_rank_what = [0 for i in range(n)]
    men_matchings = [0 for i in range(n)]
    women_matchings = [0 for i in range(n)]
    sideA = "M"
    sideB = "W"
    if F:
        temp = sideA
        sideA = sideB
        sideB = temp
    process_trace = []

    # continue until all matches made
    while curr_match_count < n:
        for man in range(n):
            # if man is single
            if men_matchings[man] == 0:
                # get first non-rejecting woman from man's preference list
                woman = mpref[man][last_rejected_by_rank_what[man]] - 1
                # both man and woman are single
                if women_matchings[woman] == 0:
                    # create match (man, woman)
                    men_matchings[man] = woman + 1
                    women_matchings[woman] = man + 1
                    curr_match_count += 1
                    process_trace.append(f"{sideA.capitalize()}{man + 1} proposed to {sideB.capitalize()}{woman + 1}, who was unmatched. They are now matched.")

                # woman is with someone
                else:
                    # find ranks of curr_partner and man given woman's preference list
                    curr_partner = women_matchings[woman]
                    curr_partner_rank = wpref[woman].index(curr_partner)
                    man_rank = wpref[woman].index(man + 1)

                    # woman prefers curr_partner over man
                    if curr_partner_rank < man_rank:
                        last_rejected_by_rank_what[man] = mpref[man].index(woman + 1) + 1
                        process_trace.append(f"{sideA.capitalize()}{man + 1} proposed to {sideB.capitalize()}{woman + 1}. Proposal rejected; prefers current match {sideA.capitalize()}{curr_partner}.")
                    # woman prefers man over curr_partner
                    else:
                        men_matchings[curr_partner - 1] = 0
                        last_rejected_by_rank_what[curr_partner - 1] = mpref[curr_partner - 1].index(woman + 1) + 1
                        men_matchings[man] = woman + 1
                        women_matchings[woman] = man + 1
                        process_trace.append(f"{sideA.capitalize()}{man + 1} proposed to {sideB.capitalize()}{woman + 1}. Proposal accepted; because {sideB.capitalize()}{woman + 1} prefers proposer {sideA.capitalize()}{man + 1} over current match {sideA.capitalize()}{curr_partner}. New pairing established. {sideA.capitalize()}{curr_partner} is now unmatch.")

    for x in range(n):
        men_matchings[x] -= 1
    men_matchings = result_format(men_matchings, sideA, sideB)
    return men_matchings, process_trace


def result_format(result, sideA="A", sideB="B"):
    formatted_result = []
    
    for i, match in enumerate(result):

        human_readable_index = i + 1
        human_readable_match = match + 1
        formatted_result.append(f"{sideA.capitalize()}{human_readable_index} is matched with {sideB.capitalize()}{human_readable_match}")
    return "; ".join(formatted_result)