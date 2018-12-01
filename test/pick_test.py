# pylint: disable=missing-docstring
from pick import Pick

VALUES = [':floke:', ':freedom:', ':piggy:', ':hamn:', ':barnvakt:',
          ':dusty_stick:', ':nohomo:', ':frybaby:', ':glitch_crab:', ':mandag:',
          ':kamerun:', ':black_square:', ':brafest:', ':slack_call:',
          ':beersdeluxe:', ':frodo:', ':kiss-my-piss:', ':hoppa:', ':yoda:',
          ':cubimal_chick:', ':bjorne:', ':andersjagare:', ':kapsyl:', ':omg:',
          ':christoffer:', ':screeching:', ':greger:', ':gratfardig:',
          ':bowtie:', ':hulk:', ':bonden:', ':rocky:', ':white_square:',
          ':shipit:', ':alex:', ':tux:', ':berith:', ':hardrocken:',
          ':stortpaket:', ':apn:', ':slack:', ':stockholmskontoret:',
          ':livsgnistan:', ':pride:', ':squirrel:', ':thumbsup_all:',
          ':simple_smile:', ':fubar:']


def _construct(max_repeat):
    return Pick(VALUES, max_repeat)


def test_pick_one():
    pick = _construct(5)
    for i in range(100):
        print("pass", i)
        result = pick.one()
        assert result in VALUES
