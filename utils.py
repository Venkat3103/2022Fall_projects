def find_phase(ball):
  """
  Computes which phase a particular ball belongs to
  :param ball: the ball number in the match
  :return: phase as a string

  >>> find_phase(4.2)
  'powerplay'
  >>> find_phase(15.2)
  'middle overs'
  >>> find_phase(18.0)
  'death overs'
  """

  if ball<=5.6:
    return "powerplay"
  elif ball<=15.6:
    return "middle overs"
  else:
    return "death overs"

