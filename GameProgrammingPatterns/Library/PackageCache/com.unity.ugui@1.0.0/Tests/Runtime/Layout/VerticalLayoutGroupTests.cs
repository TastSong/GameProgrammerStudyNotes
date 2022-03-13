using System.IO;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.UI.Tests;

namespace LayoutTests
{
    public class VerticalLayoutGroupTests : IPrebuildSetup
    {
        GameObject m_PrefabRoot;
        const string kPrefabPath = "Assets/Resources/VerticalLayoutGroupPrefab.prefab";

        private VerticalLayoutGroup m_LayoutGroup;

        public void Setup()
        {
#if UNITY_EDITOR
            var rootGO = new GameObject("rootGo");
            GameObject canvasGO = new GameObject("Canvas", typeof(RectTransform), typeof(Canvas));
            canvasGO.transform.SetParent(rootGO.transform);

            var canvas = canvasGO.GetComponent<Canvas>();
            canvas.referencePixelsPerUnit = 100;

            var groupGO = new GameObject("Group", typeof(RectTransform), typeof(VerticalLayoutGroup));
            groupGO.transform.SetParent(canvasGO.transform);

            var element1GO = new GameObject("Element1", typeof(RectTransform), typeof(LayoutElement));
            element1GO.transform.SetParent(groupGO.transform);

            var element2GO = new GameObject("Element2", typeof(RectTransform), typeof(LayoutElement));
            element2GO.transform.SetParent(groupGO.transform);

            var element3GO = new GameObject("Element3", typeof(RectTransform), typeof(LayoutElement));
            element3GO.transform.SetParent(groupGO.transform);

            VerticalLayoutGroup layoutGroup = groupGO.GetComponent<VerticalLayoutGroup>();
            layoutGroup.padding = new RectOffset(2, 4, 3, 5);
            layoutGroup.spacing = 1;
            layoutGroup.childForceExpandWidth = false;
            layoutGroup.childForceExpandHeight = false;
            layoutGroup.childControlWidth = true;
            layoutGroup.childControlHeight = true;

            var element1 = element1GO.GetComponent<LayoutElement>();
            element1.minWidth = 5;
            element1.minHeight = 10;
            element1.preferredWidth = 100;
            element1.preferredHeight = 50;
            element1.flexibleWidth = 0;
            element1.flexibleHeight = 0;
            element1.enabled = true;

            var element2 = element2GO.GetComponent<LayoutElement>();
            element2.minWidth = 10;
            element2.minHeight = 5;
            element2.preferredWidth = -1;
            element2.preferredHeight = -1;
            element2.flexibleWidth = 0;
            element2.flexibleHeight = 0;
            element2.enabled = true;

            var element3 = element3GO.GetComponent<LayoutElement>();
            element3.minWidth = 25;
            element3.minHeight = 15;
            element3.preferredWidth = 200;
            element3.preferredHeight = 80;
            element3.flexibleWidth = 1;
            element3.flexibleHeight = 1;
            element3.enabled = true;

            if (!Directory.Exists("Assets/Resources/"))
                Directory.CreateDirectory("Assets/Resources/");

            PrefabUtility.SaveAsPrefabAsset(rootGO, kPrefabPath);
            GameObject.DestroyImmediate(rootGO);
#endif
        }

        [SetUp]
        public void TestSetup()
        {
            m_PrefabRoot = Object.Instantiate(Resources.Load("VerticalLayoutGroupPrefab")) as GameObject;
            m_LayoutGroup = m_PrefabRoot.GetComponentInChildren<VerticalLayoutGroup>();
        }

        [OneTimeTearDown]
        public void TearDown()
        {
            EventSystem.current = null;
            m_LayoutGroup = null;
            Object.DestroyImmediate(m_PrefabRoot);
        }

        [OneTimeTearDown]
        public void OneTimeTearDown()
        {
#if UNITY_EDITOR
            AssetDatabase.DeleteAsset(kPrefabPath);
#endif
        }

        [Test]
        public void TestCalculateLayoutInputHorizontal()
        {
            m_LayoutGroup.CalculateLayoutInputHorizontal();
            m_LayoutGroup.SetLayoutHorizontal();
            m_LayoutGroup.CalculateLayoutInputVertical();
            m_LayoutGroup.SetLayoutVertical();

            Assert.AreEqual(31, m_LayoutGroup.minWidth);
            Assert.AreEqual(206, m_LayoutGroup.preferredWidth);
            Assert.AreEqual(1, m_LayoutGroup.flexibleWidth);
        }

        [Test]
        public void TestCalculateLayoutInputVertical()
        {
            m_LayoutGroup.CalculateLayoutInputHorizontal();
            m_LayoutGroup.SetLayoutHorizontal();
            m_LayoutGroup.CalculateLayoutInputVertical();
            m_LayoutGroup.SetLayoutVertical();

            Assert.AreEqual(40, m_LayoutGroup.minHeight);
            Assert.AreEqual(145, m_LayoutGroup.preferredHeight);
            Assert.AreEqual(1, m_LayoutGroup.flexibleHeight);
        }
    }
}
