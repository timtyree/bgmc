import numpy as np
from ._find_contours_cy import _get_contour_segments
from ._find_contours_pbc_cy import _get_contour_segments_pbc
from collections import deque

_param_options = ('high', 'low')
_mode_options = ('pbc', 'hard_boundary')

def find_contours(array, level,
                  fully_connected='low', positive_orientation='low', mode='pbc',
                  *,
                  mask=None):
    """Find iso-valued contours in a 2D array for a given level value.

    Uses the "marching squares" method to compute a the iso-valued contours of
    the input 2D array for a particular level value. Array values are linearly
    interpolated to provide better precision for the output contours.

    Parameters
    ----------
    array : 2D ndarray of double
        Input data in which to find contours.
    level : float
        Value along which to find contours in the array.
    fully_connected : str, {'low', 'high'}
         Indicates whether array elements below the given level value are to be
         considered fully-connected (and hence elements above the value will
         only be face connected), or vice-versa. (See notes below for details.)
    positive_orientation : either 'low' or 'high'
         Indicates whether the output contours will produce positively-oriented
         polygons around islands of low- or high-valued elements. If 'low' then
         contours will wind counter- clockwise around elements below the
         iso-value. Alternately, this means that low-valued elements are always
         on the left of the contour. (See below for details.)
    mask : 2D ndarray of bool, or None
        A boolean mask, True where we want to draw contours.
        Note that NaN values are always excluded from the considered region
        (``mask`` is set to ``False`` wherever ``array`` is ``NaN``).

    Returns
    -------
    contours : list of (n,2)-ndarrays
        Each contour is an ndarray of shape ``(n, 2)``,
        consisting of n ``(row, column)`` coordinates along the contour.

    Notes
    -----
    The marching squares algorithm is a special case of the marching cubes
    algorithm [1]_.  A simple explanation is available here::

      http://users.polytech.unice.fr/~lingrand/MarchingCubes/algo.html

    There is a single ambiguous case in the marching squares algorithm: when
    a given ``2 x 2``-element square has two high-valued and two low-valued
    elements, each pair diagonally adjacent. (Where high- and low-valued is
    with respect to the contour value sought.) In this case, either the
    high-valued elements can be 'connected together' via a thin isthmus that
    separates the low-valued elements, or vice-versa. When elements are
    connected together across a diagonal, they are considered 'fully
    connected' (also known as 'face+vertex-connected' or '8-connected'). Only
    high-valued or low-valued elements can be fully-connected, the other set
    will be considered as 'face-connected' or '4-connected'. By default,
    low-valued elements are considered fully-connected; this can be altered
    with the 'fully_connected' parameter.

    Output contours are not guaranteed to be closed: contours which intersect
    the array edge or a masked-off region (either where mask is False or where
    array is NaN) will be left open. All other contours will be closed. (The
    closed-ness of a contours can be tested by checking whether the beginning
    point is the same as the end point.)

    Contours are oriented. By default, array values lower than the contour
    value are to the left of the contour and values greater than the contour
    value are to the right. This means that contours will wind
    counter-clockwise (i.e. in 'positive orientation') around islands of
    low-valued pixels. This behavior can be altered with the
    'positive_orientation' parameter.

    The order of the contours in the output list is determined by the position
    of the smallest ``x,y`` (in lexicographical order) coordinate in the
    contour.  This is a side-effect of how the input array is traversed, but
    can be relied upon.

    .. warning::

       Array coordinates/values are assumed to refer to the *center* of the
       array element. Take a simple example input: ``[0, 1]``. The interpolated
       position of 0.5 in this array is midway between the 0-element (at
       ``x=0``) and the 1-element (at ``x=1``), and thus would fall at
       ``x=0.5``.

    This means that to find reasonable contours, it is best to find contours
    midway between the expected "light" and "dark" values. In particular,
    given a binarized array, *do not* choose to find contours at the low or
    high value of the array. This will often yield degenerate contours,
    especially around structures that are a single array element wide. Instead
    choose a middle value, as above.

    .. addendum::

    The aforementioned ambiguity is resolved according to the natural reduction
    of the method presented in [2] to two spatial dimensions.

    References
    ----------
    .. [1] Lorensen, William and Harvey E. Cline. Marching Cubes: A High
           Resolution 3D Surface Construction Algorithm. Computer Graphics
           (SIGGRAPH 87 Proceedings) 21(4) July 1987, p. 163-170).
    .. [2] Thomas Lewiner, Helio Lopes, Antonio Wilson Vieira and Geovan
           Tavares. Efficient implementation of Marching Cubes' cases with
           topological guarantees. Journal of Graphics Tools 8(2)
           pp. 1-15 (december 2003).
           :DOI:`10.1080/10867651.2003.10487582`


    Examples
    --------
    >>> a = np.zeros((3, 3))
    >>> a[0, 0] = 1
    >>> a
    array([[1., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.]])
    >>> find_contours(a, 0.5)
    [array([[0. , 0.5],
           [0.5, 0. ]])]
    """
    if fully_connected not in _param_options:
        raise ValueError('Parameters "fully_connected" must be either '
                         '"high" or "low".')
    if positive_orientation not in _param_options:
        raise ValueError('Parameters "positive_orientation" must be either '
                         '"high" or "low".')
    if mode not in _mode_options:
        raise ValueError('Parameters "positive_orientation" must be either '
                         '"pbc" or "hard_boundary".')
    if array.shape[0] < 2 or array.shape[1] < 2:
        raise ValueError("Input array must be at least 2x2.")
    if array.ndim != 2:
        raise ValueError('Only 2D arrays are supported.')
    if mask is not None:
        if mask.shape != array.shape:
            raise ValueError('Parameters "array" and "mask"'
                             ' must have same shape.')
        if not np.can_cast(mask.dtype, bool, casting='safe'):
            raise TypeError('Parameter "mask" must be a binary array.')
        mask = mask.astype(np.uint8, copy=False)

    if mode == 'pbc':
        segments = _get_contour_segments_pbc(array.astype(np.double), float(level), mask=mask)
        contours = _assemble_contours(segments)
    if mode == 'hard_boundary':
        segments = _get_contour_segments(array.astype(np.double), float(level), mask=mask)
        contours = _assemble_contours(segments)
    if positive_orientation == 'high':
        contours = [c[::-1] for c in contours]
    return contours

def _assemble_contours(segments):
    current_index = 0
    contours = {}
    starts = {}
    ends = {}
    for from_point, to_point in segments:
        # Ignore degenerate segments.
        # This happens when (and only when) one vertex of the square is
        # exactly the contour level, and the rest are above or below.
        # This degenerate vertex will be picked up later by neighboring
        # squares.
        if from_point == to_point:
            continue

        tail, tail_num = starts.pop(to_point, (None, None))
        head, head_num = ends.pop(from_point, (None, None))

        if tail is not None and head is not None:
            # We need to connect these two contours.
            if tail is head:
                # We need to closed a contour.
                # Add the end point
                head.append(to_point)
            else:  # tail is not head
                # We need to join two distinct contours.
                # We want to keep the first contour segment created, so that
                # the final contours are ordered left->right, top->bottom.
                if tail_num > head_num:
                    # tail was created second. Append tail to head.
                    head.extend(tail)
                    # remove all traces of tail:
                    ends.pop(tail[-1])
                    contours.pop(tail_num, None)
                    # Update contour starts end ends
                    starts[head[0]] = (head, head_num)
                    ends[head[-1]] = (head, head_num)
                else:  # tail_num <= head_num
                    # head was created second. Prepend head to tail.
                    tail.extendleft(reversed(head))
                    # remove all traces of head:
                    starts.pop(head[0])
                    contours.pop(head_num, None)
                    # Update contour starts end ends
                    starts[tail[0]] = (tail, tail_num)
                    ends[tail[-1]] = (tail, tail_num)
        elif tail is None and head is None:
            # we need to add a new contour
            new_contour = deque((from_point, to_point))
            contours[current_index] = new_contour
            starts[from_point] = (new_contour, current_index)
            ends[to_point] = (new_contour, current_index)
            current_index += 1
        elif head is None:  # tail is not None
            # We've found a single contour to which the new segment should be
            # prepended.
            tail.appendleft(from_point)
            starts[from_point] = (tail, tail_num)
        else:  # tail is None and head is not None:
            # We've found a single contour to which the new segment should be
            # appended
            head.append(to_point)
            ends[to_point] = (head, head_num)

    return [np.array(contour) for _, contour in sorted(contours.items())]
