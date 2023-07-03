def no_heuristic(state):
    '''
        This function uses no computation at all and just returns 0 (Dijkstra's algorithm)

        Returns:
            (int) : a zero.
    '''
    return 0
def wagdy_heuristic(state):
    '''
    For each successive pair of balls that are not the same color, add an estimated cost of 2.

    Parameters:
        state (State): current state of the game.

    Returns:
        f (int): the heuristic's value.
    '''

    total_cost = 0

    # Iterate over each tube in the state
    for tube in state.tubes:
        tube_length = len(tube)

        # Iterate over each pair of successive balls in the tube
        for i in range(tube_length - 1):
            ball1 = tube[i]
            ball2 = tube[i + 1]

            # Check if the pair of balls is different in color
            if ball1 != ball2:
                total_cost += 2

    return total_cost


def repeated_color_heuristic(state):
    '''
    For each ball that is not the same color as the most repeated color in a tube, add an estimated cost of 1.

    Returns:
        f (int): the heuristic's value.
    '''
    cost = 0

    for tube in state.tubes:
        colors_count = {}
        max_count = 0
        max_color = None

        # Count the number of occurrences of each color in the tube
        for ball in tube:
            if ball != 0:
                if ball in colors_count:
                    colors_count[ball] += 1
                else:
                    colors_count[ball] = 1

                # Update the maximum count and color
                if colors_count[ball] > max_count:
                    max_count = colors_count[ball]
                    max_color = ball

        # Add the cost for balls that don't have the same color as the most repeated color
        for ball in tube:
            if ball != 0 and ball != max_color:
                cost += 1

    return cost

