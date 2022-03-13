using System.Collections.Generic;

namespace UnityEngine.UI
{
    /// <summary>
    /// Utility class to help when clipping using IClipper.
    /// </summary>
    public static class Clipping
    {
        /// <summary>
        /// Find the Rect to use for clipping.
        /// Given the input RectMask2ds find a rectangle that is the overlap of all the inputs.
        /// </summary>
        /// <param name="rectMaskParents">RectMasks to build the overlap rect from.</param>
        /// <param name="validRect">Was there a valid Rect found.</param>
        /// <returns>The final compounded overlapping rect</returns>
        public static Rect FindCullAndClipWorldRect(List<RectMask2D> rectMaskParents, out bool validRect)
        {
            if (rectMaskParents.Count == 0)
            {
                validRect = false;
                return new Rect();
            }

            Rect current = rectMaskParents[0].canvasRect;
            Vector4 offset = rectMaskParents[0].padding;
            float xMin = current.xMin + offset.x;
            float xMax = current.xMax - offset.z;
            float yMin = current.yMin + offset.y;
            float yMax = current.yMax - offset.w;
            for (var i = 1; i < rectMaskParents.Count; ++i)
            {
                current = rectMaskParents[i].canvasRect;
                offset = rectMaskParents[i].padding;
                if (xMin < current.xMin + offset.x)
                    xMin = current.xMin + offset.x;
                if (yMin < current.yMin + offset.y)
                    yMin = current.yMin + offset.y;
                if (xMax > current.xMax - offset.z)
                    xMax = current.xMax - offset.z;
                if (yMax > current.yMax - offset.w)
                    yMax = current.yMax - offset.w;
            }

            validRect = xMax > xMin && yMax > yMin;
            if (validRect)
                return new Rect(xMin, yMin, xMax - xMin, yMax - yMin);
            else
                return new Rect();
        }
    }
}
