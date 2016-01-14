# coding=utf-8
__author__ = 'ashishgagneja'

import sys

import larkin.shared.utils


def score_occ_similarity(base_dt, date_shortlist, occ_ts, timezone):
    """
    Score occupancy profile similarity between occupancy predicted for base date
    and that observed on the the short list of dates provided

    :param base_dt: datetime.date
        base date or as of date
    :param date_shortlist: list
        short-list of dates to choose from
    :param occ_ts: pandas Series
        occupancy data
    :param timezone: pytz.timezone
        target timezone or building timezone
    :return: list of tuples sorted by score
        each tuple is of the form (<date>, <similarity_score>)
    """

    # TODO: when we have occupancy forecast, use that to obtain expected
    # occupancy. For now, use actual
    base_ts = larkin.shared.utils.get_dt_tseries(base_dt, occ_ts, timezone)
    base_ts_nodatetz = larkin.shared.utils.drop_series_ix_date(base_ts)

    scores = []
    for dt_t in date_shortlist:

        score = larkin.shared.utils.compute_profile_similarity_score(
                    base_ts_nodatetz,
                    larkin.shared.utils.drop_series_ix_date(
                        larkin.shared.utils.get_dt_tseries(dt_t, occ_ts,
                                                           timezone)))

        scores.append((dt_t, score))

    scores.sort(key=lambda x: x[1] if x[1] else sys.maxsize)
    return scores