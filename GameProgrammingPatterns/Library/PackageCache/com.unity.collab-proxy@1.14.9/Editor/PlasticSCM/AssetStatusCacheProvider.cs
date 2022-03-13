using System;

using Unity.PlasticSCM.Editor.AssetsOverlays.Cache;
using Codice.CM.Common;

namespace Unity.PlasticSCM.Editor
{
    internal static class AssetStatusCacheProvider
    {
        internal static IAssetStatusCache Get(WorkspaceInfo wkInfo,
            bool isGluonMode,
            Action repaintProjectWindow)
        {
            if (sAssetStatusCache == null)
            {
                sAssetStatusCache =
                   new AssetStatusCache(
                       wkInfo,
                       isGluonMode,
                       repaintProjectWindow);
            }
            return sAssetStatusCache;
        }

        static IAssetStatusCache sAssetStatusCache;
    }
 }
