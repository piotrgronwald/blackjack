import random, sys

HEARTS   = chr(9829) # Znak 9829 to '♥'.
DIAMONDS = chr(9830) # Znak 9830 to '♦'.
SPADES   = chr(9824) # Znak 9824 to '♠'.
CLUBS    = chr(9827) # Znak 9827 to '♣'.
BACKSIDE = 'tył'


def main():
    print(''' Oczko
    Zasady:
      Spróbuj uzyskać liczbę punktów jak najbardziej zbliżoną do 21, ale nie większą.
      Króle, Damy i Walety mają 10 punktów.
      Asy mają 1 lub 11 punktów.
      Karty od 2 do 10 mają odpowiednią do swojego numeru liczbę punktów.
      Naciśnij H, by wziąć kolejną kartę.
      Klawisz S zatrzymuje dobieranie kart.
      Przy swojej pierwszej rozgrywce możesz wcisnąć P, by podwoić swój zakład,
      ale musisz to zrobić dokładnie jeden raz przed zakończeniem dobierania kart.
      W przypadku remisu, postawiona kwota jest zwracana graczowi.
      Krupier kończy dobierać karty przy wartości 17''')

    money = 5000
    while True:
        if money <= 0:
            print("Jesteś spłukany!")
            print("Dobrze, że nie grałeś na prawdziwe pieniądze.")
            print('Dziękuję za grę!')
            sys.exit()

        print('Budżet:', money)
        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print('Zakład:', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break

            move = getMove(playerHand, money - bet)

            if move == 'P':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Zakład zwiększony do kwoty {}.'.format(bet))
                print('Zakład:', bet)

            if move in ('D', 'P'):
                newCard = deck.pop()
                rank, suit = newCard
                print('Wziąłeś {} {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('S', 'P'):
                break

        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Krupier dobiera kartę...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input('Naciśnij Enter, by kontynuować...')
                print('\n\n')

        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        if dealerValue > 21:
            print('Krupier przekroczył 21! Wygrałeś {} PLN!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('Przegrałeś!')
            money -= bet
        elif playerValue > dealerValue:
            print('Wygrałeś {} PLN!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Jest remis, zakład wraca do Ciebie.')

        input('Naciśnij Enter, by kontynuować...')
        print('\n\n')


def getBet(maxBet):
    while True:
        print('Ile chcesz postawić? (1-{} lub KONIEC)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'KONIEC':
            print('Dziękuję za grę!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet


def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print('KRUPIER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('KRUPIER: ???')
        displayCards([BACKSIDE] + dealerHand[1:])

    print('GRACZ:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def getMove(playerHand, money):
    while True:
        moves = ['(D)obierz', '(S)top']

        if len(playerHand) == 2 and money > 0:
            moves.append('(P)odwój')

        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('D', 'S'):
            return move
        if move == 'P' and '(P)odwój' in moves:
            return move


if __name__ == '__main__':
    main()
