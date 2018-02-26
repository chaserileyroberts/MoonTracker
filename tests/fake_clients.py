
class twilio_fake():

    def __init__(self):
        self.to = []
        self.messages = []

    def send_message(self, to, from_, body):
        self.to.append(to)
        self.messages.append(body)


class price_tracker_fake():

    def __init__(self, amount):
        self.amount = float(amount)

    def get_spot_price(self, asset):
        return self.amount
