using Codice.CM.Common;
using PlasticGui;
using Unity.PlasticSCM.Editor.AssetMenu;
using Unity.PlasticSCM.Editor.AssetsOverlays;
using Unity.PlasticSCM.Editor.AssetsOverlays.Cache;
using Unity.PlasticSCM.Editor.UI;
using UnityEditor;
using UnityEngine;

namespace Unity.PlasticSCM.Editor
{
    [InitializeOnLoad]
    class DelayedInitializeOnLoadHandler
    {
        static DelayedInitializeOnLoadHandler()
        {
            CooldownWindowDelayer cooldownInitializeAction = new CooldownWindowDelayer(
                DelayedInitialization, UnityConstants.ASSET_MENU_DELAYED_INITIALIZE_INTERVAL);

            cooldownInitializeAction.Ping();
        }

        internal static void DelayedInitialization()
        {
            PlasticApp.InitializeIfNeeded();

            if (sPlasticAPI == null)
                sPlasticAPI = new PlasticAPI();

            WorkspaceInfo wkInfo = FindWorkspace.InfoForApplicationPath(
                Application.dataPath,
                sPlasticAPI);

            if (wkInfo == null)
                return;

            AssetMenuItems.Enable(sPlasticAPI, wkInfo);
            
            IAssetStatusCache assetStatusCache = AssetStatusCacheProvider.Get(
                wkInfo,
                sPlasticAPI.IsGluonWorkspace(wkInfo),
                ProjectWindow.Repaint);
            
            DrawAssetOverlay.Initialize(sPlasticAPI, assetStatusCache, ProjectWindow.Repaint);
        }

        static PlasticAPI sPlasticAPI;
    }
}
