# Fusion commands: name, identifier, API, Personal, tested

List of the 1 665 commands of the Fusion user interface (Italian UI, Nov. 2026), matched to the API where it exists. **Do not read it whole**: search for the command's Italian UI name or its identifier (`Ctrl+F`/Grep). «API —» = no matched API object: the command is used from the user interface. «Tested» = the API object appears in the code of the tested recipes (this does not guarantee every variant).

## Index

- Design / SOLIDO tab (`SolidTab`): 163
- Design / SUPERFICIE tab (`SurfaceTab`): 20
- Design / Mesh tab (`ParaMeshOuterTab`): 29
- Design / FORMA tab (`FormTab`): 48
- Design / LAMIERA tab (`SheetMetalTab`): 17
- Design / PLASTICA tab (`PlasticTab`): 7
- Design / ASSIEME tab (`AssemblyTab`): 1
- Design / GESTISCI tab (`ManageTab`): 9
- Design / UTILITÀ tab (`ToolsTab`): 11
- Design / AUTOMAZIONE tab (`AutomationTab`): 2
- Design / PCB tab (`PCBTab`): 7
- Design / Pacchetto tab (`Package3DTab`): 48
- Design / SOLIDO tab (`BasefeatureSolidTab`): 1
- Design / SCHIZZO tab (`SketchTab`): 67
- Design / POSIZIONE tab (`EditSnapshotTab`): 2
- Design / Modifica diretta della mesh tab (`ParaMeshBaseFeatureTab`): 1
- Design / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 446
- Manufacture (CNC) / Fresatura tab (`MillingTab`): 88
- Manufacture (CNC) / Tornitura tab (`TurningTab`): 17
- Manufacture (CNC) / Additivo tab (`AdditiveTab`): 43
- Manufacture (CNC) / Risultati tab (`AdditiveResultsTab`): 8
- Manufacture (CNC) / Ispezione tab (`ProbingTab`): 14
- Manufacture (CNC) / Fabbricazione tab (`FabricationTab`): 7
- Manufacture (CNC) / Utilità tab (`UtilitiesTab`): 3
- Manufacture (CNC) / Allineamento parte tab (`PartAlignmentTab`): 8
- Manufacture (CNC) / Allineamento parte in tempo reale tab (`LiveAlignmentTab`): 3
- Manufacture (CNC) / Simulazione tab (`SimulationTab`): 12
- Manufacture (CNC) / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 207
- Drawing / DISEGNO tab (`FusionDocTab`): 103
- Drawing / COMPONENTI ELETTRONICI tab (`ElectronicsTab`): 5
- Drawing / GESTISCI tab (`ManageTab`): 1
- Drawing / CARTIGLIO tab (`TitleBlockTab`): 8
- Drawing / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 79
- Rendering / RENDERING tab (`RenderTab`): 9
- Rendering / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 4
- Animation / ANIMAZIONE tab (`Animation`): 10
- Animation / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 29
- Common (File menu and fixed toolbars) / Menus (File, fixed toolbars, right-click, radial) (`Menu`): 128

## Design / SOLIDO tab (`SolidTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Crea schizzo | `SketchCreate` | `Sketches` | yes (available) | yes |
| Crea forma | `TSplineBaseFeatureCreationCommand` | `FormFeatures.add` | yes (available) | yes |
| Deriva | `PushDeriveCommand` | `DeriveFeatures` | yes (available) | yes |
| Modellazione automatica | `AutomatedModelingCommand` | — | automated / generative modeling: no | — |
| Estrusione | `Extrude` | `ExtrudeFeatures` | yes (available) | yes |
| Rivoluzione | `Revolve` | `RevolveFeatures` | yes (available) | yes |
| Sweep | `Sweep` | `SweepFeatures` | yes (available) | yes |
| Loft | `SolidLoft` | `LoftFeatures` | yes (available) | yes |
| Nervatura | `FusionRibCommand` | `RibFeatures` | yes (available) | yes |
| Maglia | `FusionWebCommand` | `WebFeatures` | yes (available) | no |
| Sbalzo | `EmbossCmd` | `EmbossFeatures` | yes (available) | yes |
| Foratura | `FusionHoleCommand` | `HoleFeatures` | yes (available) | yes |
| Filettatura | `FusionThreadCommand` | `ThreadFeatures` | yes (available) | yes |
| Parallelepipedo | `PrimitiveBox` | `BoxFeatures` | yes (available) | no |
| Cilindro | `PrimitiveCylinder` | `CylinderFeatures` | yes (available) | no |
| Sfera | `PrimitiveSphere` | `SphereFeatures` | yes (available) | no |
| Toroide | `PrimitiveTorus` | `TorusFeatures` | yes (available) | no |
| Elicoide | `PrimitiveCoil` | `CoilFeatures` | yes (available) | yes |
| Tubo | `PrimitivePipe` | `PipeFeatures` | yes (available) | yes |
| Solido di delimitazione | `StockModelCommand` | — | yes (available) | — |
| Serie rettangolare | `PatternRectangular` | `RectangularPatternFeatures` | yes (available) | yes |
| Serie circolare | `PatternCircular` | `CircularPatternFeatures` | yes (available) | yes |
| Serie su traiettoria | `PatternOnPath` | `PathPatternFeatures` | yes (available) | yes |
| Serie geometrica | `FusionPatternGeometricCommand` | — | yes (available) | — |
| Specchio | `MirrorCommand` | `MirrorFeatures` | yes (available) | yes |
| Ispessisci | `FusionSurfaceThickenCommand` | `ThickenFeatures` | yes (available) | yes |
| Riempimento contorno | `SurfaceSculpt` | `BoundaryFillFeatures` | yes (available) | no |
| Trova lavorazioni | `FusionFindFeaturesCommand` | — | yes (available) | — |
| Volume fluido | `EnclosureCommand` | — | yes (available) | — |
| Crea lavorazione di base | `BaseFeatureCreationCommand` | `BaseFeatures` | yes (available) | yes |
| Crea PCB collegato | `PCBExternalComponentCreationCmd` | — | yes (available) | — |
| Deriva PCB | `PCBDeriveCmd` | — | yes (available) | — |
| Crea PCB non collegato | `PCBCreateCmd` | — | yes (available) | — |
| Origine del giunto | `JointOrigin` | `JointOrigins` | yes (available) | yes |
| Genera timeline | `TimelineBuilderCommand` | `Timeline` | yes (available) | yes |
| Premere e trascinare | `FusionPressPullCommand` | `ExtrudeFeatures` | yes (available) | yes |
| Modifica faccia | `EditFaceCommand` | — | yes (available) | — |
| Raccordo | `FusionFilletEdgesCommand` | `FilletFeatures` | yes (available) | yes |
| Smusso | `FusionChamferCommand` | `ChamferFeatures` | yes (available) | yes |
| Svuotamento | `FusionShellBodyCommand` | `ShellFeatures` | yes (available) | yes |
| Sformo | `FusionDraftCommand` | `DraftFeatures` | yes (available) | yes |
| Scala | `ModifyScale` | `ScaleFeatures` | yes (available) | yes |
| Combina | `FusionCombineCommand` | `CombineFeatures` | yes (available) | yes |
| Offset faccia | `FusionOffsetFacesCommand` | `OffsetFacesFeatures` | yes (available) | yes |
| Sostituisci faccia | `FusionReplaceFaceCommand` | `ReplaceFaceFeatures` | yes (available) | no |
| Divisione faccia | `FusionSplitFaceCommand` | `SplitFaceFeatures` | yes (available) | yes |
| Divisione corpo | `FusionSplitBodyCommand` | `SplitBodyFeatures` | yes (available) | yes |
| Divisione sagoma | `FusionPartingLineSplitCmd` | `SilhouetteSplitFeatures` | yes (available) | no |
| Sposta/Copia | `FusionMoveCommand` | `MoveFeatures` | yes (available) | yes |
| Allinea | `AlignCmd` | — | yes (available) | — |
| Elimina | `FusionDeleteCommand` | `Design.deleteEntities` | yes (available) | no |
| Rimuovi | `SoftDeleteCommand` | `RemoveFeatures` | yes (available) | no |
| Disponi | `ArrangeCommand` | `ArrangeFeatures` | yes (available) | no |
| Rimuovi lavorazioni | `FusionRemoveFeaturesCommand` | `RemoveFeatures` | yes (available) | no |
| Rimuovi facce | `FusionRemoveFacesCommand` | `RemoveFeatures` | yes (available) | no |
| Sostituisci con primitive | `ReplaceWithPrimitivesCommand` | — | yes (available) | — |
| Reticolo volumetrico | `VolFieldCreateLatticeCommand` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Texture volumetrica | `VolFieldTextureCommand` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Materiale fisico | `PhysicalMaterialCommand` | `Materials` | yes (available) | yes |
| Aspetto | `AppearanceCommand` | `Appearances` | yes (available) | yes |
| Gestione dei materiali | `MaterialCommand` | `Materials` | yes (available) | yes |
| Modifica parametri | `ChangeParameterCommand` | `UserParameters` | yes (available) | yes |
| Calcola tutto | `FusionComputeAllCommand` | `Design` | yes (available) | yes |
| Calcola irrisolti | `FusionComputeUnresolvedCommand` | `Design` | yes (available) | yes |
| Converti | `TSpline2BRepCommand` | `FormFeature.updateBRep` | yes (available) | no |
| Distinta componenti | `MaterializedBomHybridCmd` | — | bill of materials and releases (Manage): no | — |
| Inserisci componente | `FusionImportCommandFromToolbar` | `ImportManager` | yes (available) | yes |
| Nuovo componente | `FusionCreateNewComponentCommand` | `Occurrences` | yes (available) | yes |
| Duplica con giunti | `FusionDuplicateWithJointsCommand` | — | yes (available) | — |
| Vincola componenti | `AssemblyMateCommand` | `AssemblyConstraints 🧪` | yes (available) | no |
| Vincolo di allineamento | `AlignConstraintCmd` | `AssemblyConstraints 🧪` | yes (available) | no |
| Vincolo dell'angolo | `AngleConstraintCmd` | `AssemblyConstraints 🧪` | yes (available) | no |
| Vincolo centro | `MidplaneConstraintCmd` | `AssemblyConstraints 🧪` | yes (available) | no |
| Vincolo tangente | `TangentConstraintCmd` | `AssemblyConstraints 🧪` | yes (available) | no |
| Vincolo giunto | `JointConstraintCmd` | `AssemblyConstraints 🧪` | yes (available) | no |
| Giunto | `JointAssembleCmdNew` | `Joints` | yes (available) | yes |
| Giunto come costruito | `JointAsBuiltCmd` | `AsBuiltJoints` | yes (available) | yes |
| Vincolo come costruito | `AsBuiltConstraintCmd` | `AsBuiltJoints` | yes (available) | yes |
| Gruppo rigido | `RigidGroupCmd` | `RigidGroups` | yes (available) | yes |
| Aziona giunti | `FusionMoveJointsCommand` | `Joint.jointMotion` | yes (available) | yes |
| Collegamento movimento | `FusionMotionRelationshipCommand` | `MotionLinks` | yes (available) | no |
| Studio del movimento | `FusionMotionStudyCommand` | — | yes (available) | — |
| Abilita gruppi di contatti | `EnableContactSetsCmd` | `Design.isContactSetAnalysis` | yes (available) | no |
| Abilita tutti i contatti | `EnableAllContactCmd` | `Design.isContactAnalysisEnabled` | yes (available) | no |
| Disabilita contatto | `DisableAllContactCmd` | `Design.isContactAnalysisEnabled` | yes (available) | no |
| Nuovo gruppo di contatti | `ContactSetCmd` | `ContactSets` | yes (available) | no |
| Configura | `FusionStartDesignConfigModeCmd` | — | configurations: no | — |
| Visualizza tabella di configurazione | `FusionShowDesignConfigPanelCmd` | — | configurations: no | — |
| Crea regole di configurazione | `FusionConfigurationRulesCmd` | — | configurations: no | — |
| Sistema di coordinate utente (UCS) | `CoordinateSystemCommand` | — | yes (available) | — |
| Piano di offset | `ConstructionPlaneOffsetFromPlaneCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano in corrispondenza dell'angolo | `ConstructionPlaneAtAngleCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano tangente | `ConstructionTangentPlaneCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano medio | `ConstructionMidPlaneCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano perpendicolare | `ConstructionPlanePerpendicularToPlaneCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano attraverso due spigoli | `ConstructionPlaneFromTwoEdgesCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano attraverso tre punti | `ConstructionPlaneFromThreePointsCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Piano lungo la traiettoria | `ConstructionPlaneAlongPathCommand` | `ConstructionPlaneInput` | yes (available) | no |
| Asse attraverso cilindro/cono/toroide | `ConstructionAxisThroughCylinderCommand` | `ConstructionAxisInput` | yes (available) | no |
| Asse perpendicolare alla faccia | `ConstructionAxisNormalToFaceCommand` | `ConstructionAxisInput` | yes (available) | no |
| Asse tra due piani | `ConstructionAxisFromTwoPlanesCommand` | `ConstructionAxisInput` | yes (available) | no |
| Asse attraverso due punti | `ConstructionAxisThroughTwoPointsCommand` | `ConstructionAxisInput` | yes (available) | no |
| Asse attraverso spigolo | `ConstructionAxisThroughEdgeCommand` | `ConstructionAxisInput` | yes (available) | no |
| Punto in corrispondenza di un vertice | `ConstructionPointFromPointCommand` | `ConstructionPointInput` | yes (available) | no |
| Punto attraverso due spigoli | `ConstructionPointThroughTwoEdgesCommand` | `ConstructionPointInput` | yes (available) | no |
| Punto attraverso tre piani | `ConstructionPointFromThreePlanesCommand` | `ConstructionPointInput` | yes (available) | no |
| Punto al centro del cerchio/della sfera/del toroide | `ConstructionPointFromCircleOrSphereCommand` | `ConstructionPointInput` | yes (available) | no |
| Punto in corrispondenza di uno spigolo e di un piano | `ConstructionPointAtEdgeAndPlaneCommand` | `ConstructionPointInput` | yes (available) | no |
| Punto lungo la traiettoria | `ConstructionPointAlongPathCommand` | `ConstructionPointInput` | yes (available) | no |
| Misura | `MeasureCommand` | `MeasureManager` | yes (available) | yes |
| Analisi sezione | `FusionHalfSectionViewCommand` | `SectionAnalyses` | yes (available) | yes |
| Interferenza | `InterferenceCheckCommand` | `InterferenceInput` | yes (available) | no |
| Centro di massa | `FusionCenterOfMassCommand` | `PhysicalProperties.centerOfMass` | yes (available) | yes |
| Analisi pettini di curvatura | `FusionCurvatureCombAnalysisCommand` | `CurvatureCombAnalyses` | yes (available) | no |
| Analisi mappa curvatura | `FusionCurvatureMapAnalysisCommand` | `CurvatureMapAnalyses` | yes (available) | no |
| Analisi sformo | `FusionDraftAnalysisCommand` | `DraftAnalyses` | yes (available) | yes |
| Analisi mappa ambiente | `FusionEnvironmentMapAnalysisCommand` | `EnvironmentMapAnalyses` | yes (available) | no |
| Analisi isocurva | `FusionIsoCurveAnalysisCommand` | `IsoCurveAnalyses` | yes (available) | no |
| Analisi Zebra | `FusionZebraAnalysisCommand` | `ZebraAnalyses` | yes (available) | no |
| Convalida | `FusionSurfaceValidateCommand` | — | yes (available) | — |
| Analisi accessibilità | `FusionAccessibilityAnalysisCommand` | `AccessibilityAnalyses` | yes (available) | yes |
| Analisi raggio minimo | `FusionMinimumRadiusAnalysisCommand` | `MinimumRadiusAnalyses` | yes (available) | yes |
| Analisi connessione componente | `FusionComponentConnectionAnalysisCommand` | — | yes (available) | — |
| Analisi della pila di elementi di fissaggio | `FusionFastenerStackAnalysisCommand` | — | yes (available) | — |
| Navigatore | `GraphViewCmd` | — | yes (available) | — |
| Analisi GDL | `FusionDOFAnalysisCommand` | — | yes (available) | — |
| Modifica analisi connessione componente | `FusionEditComponentConnectionAnalysisCommand` | — | yes (available) | — |
| Visualizza colori componenti | `FusionViewColorCyclingToggleCmd` | — | yes (available) | — |
| Visualizza gruppi di facce mesh | `FacegroupsToggleCmd` | `MeshBodyDisplayOverrides.isSuppressFaceGroupColors` | yes (available) | no |
| Statistiche assieme | `FusionAssemblyStatisticsCommand` | — | yes (available) | — |
| Trova componenti simili | `SimilarPartsCommand` | — | yes (available) | — |
| Cronologia | `ShowHistoryToolbarCmd` | — | yes (available) | — |
| Riepilogo modifiche | `ShowChangeAwarenessToolbarCmd` | — | yes (available) | — |
| Sustainability Insights | `GravityClimate_ManufacturingSustainabilityInsights_MainDialog` | — | yes (available) | — |
| Decalcomania | `FusionAddEditDecalCommand` | `Decals` | yes (available) | no |
| Area grafica | `FusionAddCanvasCommand` | `Canvases` | yes (available) | yes |
| Inserisci T-spline | `TSplineImportCommand` | `TSplineBodies.addByTSMFile` | yes (available) | no |
| Inserisci SVG | `SketchImportSVG` | `Sketch.importSVG` | yes (available) | yes |
| Inserisci file DXF | `ImportDxfFileCommand` | `ImportManager` | yes (available) | yes |
| Inserisci mesh | `ParaMeshInsertAlignCommand` | `MeshBodies` | yes (available) | yes |
| Inserisci elemento di fissaggio | `FusionFastenersCommand` | — | yes (available) | — |
| Inserisci derivazione | `PullDeriveCommand` | `DeriveFeatures` | yes (available) | yes |
| Inserisci componente McMaster-Carr | `InsertMcMasterCarrComponentCommand` | — | yes (available) | — |
| Inserisci una parte produttore | `cadenasparts4cad` | — | yes (available) | — |
| Inserire i componenti fornitore di TraceParts | `traceparts_insert` | — | yes (available) | — |
| Aggiungi ad assieme | `NewAssemblyFromPartCommand` | `Occurrences` | yes (available) | yes |
| Seleziona | `SelectCommand` | `Selections` | yes (available) | no |
| Selezione con riquadro | `selectWindow` | `Selections` | yes (available) | no |
| Selezione a forma libera | `selectFreeForm` | `Selections` | yes (available) | no |
| Selezione a pennello | `selectPaint` | `Selections` | yes (available) | no |
| Seleziona per nome | `SelectByNameCommand` | `Selections` | yes (available) | no |
| Seleziona in base a contorno | `SelectByBoundaryCommand` | `Selections` | yes (available) | no |
| Seleziona per dimensione | `FusionSelectBodiesBySizeCommand` | `Selections` | yes (available) | no |
| Inverti selezione | `SelectByInvertCommand` | `Selections` | yes (available) | no |
| Origine e contorno | `FusionSelectSeedAndBoundaryFacesCommand` | `Selections` | yes (available) | no |
| Trascinamento componenti | `FusionDragCompControlsCmd` | — | yes (available) | — |
| Priorità selezione corpo | `SelectBodyPriorityCommand` | `Selections` | yes (available) | no |
| Priorità selezione facce | `SelectFacePriorityCommand` | `Selections` | yes (available) | no |
| Priorità selezione spigolo | `SelectEdgePriorityCommand` | `Selections` | yes (available) | no |
| Priorità selezione componente | `SelectComponentPriorityCommand` | `Selections` | yes (available) | no |
| Filtri di selezione | `SelectionFilterCommand` | `Selections` | yes (available) | no |
| Acquisizione della posizione | `SnapshotCmd` | `Snapshots` | yes (available) | no |
| Ripristina posizione | `AsBuiltPositionsCmd` | `Snapshots.revertPendingSnapshot` | yes (available) | no |

## Design / SUPERFICIE tab (`SurfaceTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Estrusione | `SurfaceExtrude` | `ExtrudeFeatures` | yes (available) | yes |
| Rivoluzione | `SurfaceRevolve` | `RevolveFeatures` | yes (available) | yes |
| Sweep | `SurfaceSweep` | `SweepFeatures` | yes (available) | yes |
| Loft | `SurfaceLoft` | `LoftFeatures` | yes (available) | yes |
| Delimita | `FusionSurfacePatchCommand` | `PatchFeatures` | yes (available) | yes |
| Rigata | `FusionSurfaceRuledCommand` | `RuledSurfaceFeatures` | yes (available) | no |
| Offset | `FusionSurfaceOffsetCommand` | `OffsetFeatures` | yes (available) | no |
| Parallelepipedo | `SurfPrimitiveBox` | — | yes (available) | — |
| Cilindro | `SurfPrimitiveCylinder` | — | yes (available) | — |
| Sfera | `SurfPrimitiveSphere` | — | yes (available) | — |
| Toroide | `SurfPrimitiveTorus` | — | yes (available) | — |
| Elicoide | `SurfPrimitiveCoil` | — | yes (available) | — |
| Tubo | `SurfPrimitivePipe` | — | yes (available) | — |
| Ritaglia | `FusionSurfaceTrimCommand` | `TrimFeatures` | yes (available) | no |
| Annulla taglio | `FusionSurfaceUntrimCommand` | `UntrimFeatures` | yes (available) | no |
| Estendi | `FusionExtendCommand` | `ExtendFeatures` | yes (available) | yes |
| Unisci | `FusionSurfaceStitchCommand` | `StitchFeatures` | yes (available) | yes |
| Separa | `FusionSurfaceUnStitchCommand` | `UnstitchFeatures` | yes (available) | no |
| Unisci | `FusionSurfaceMergeCommand` | `MergeFacesFeatures` | yes (available) | no |
| Inverti normale | `FusionSurfaceReverseNormalCommand` | `ReverseNormalFeatures` | yes (available) | no |

## Design / Mesh tab (`ParaMeshOuterTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Tessellazione | `ParaMeshTessellateCommand` | `MeshBodies.addByTriangleMeshData` | yes (available) | no |
| Crea schizzo sezione mesh | `ParaMeshPlanarSectionCommand` | — | yes (available) | — |
| Crea lavorazione mesh di base | `ParaMeshEmptyBaseFeatureCommand` | `BaseFeatures` | yes (available) | yes |
| Ripristina | `ParaMeshRepairCommand` | `MeshRepairFeatures 🧪` | yes (available) | yes |
| Genera gruppi di facce | `ParaMeshCalculateFaceGroupsCommand` | `MeshGenerateFaceGroupsFeatures 🧪` | yes (available) | yes |
| Combina gruppi facce | `ParaMeshMergeFaceGroupsCommand` | `MeshCombineFaceGroupsFeatures 🧪` | yes (available) | yes |
| Crea gruppo facce | `ParaMeshCreateFaceGroupCommand` | — | yes (available) | — |
| Modifica diretta | `ParaMeshBaseFeatureCreateCommand` | `BaseFeatures` | yes (available) | yes |
| Rigenera mesh | `ParaMeshRemeshCommand` | `MeshRemeshFeatures 🧪` | yes (available) | yes |
| Riduci | `ParaMeshReduceCommand` | `MeshReduceFeatures 🧪` | yes (available) | yes |
| Taglio piano | `ParaMeshPlaneCutCommand` | — | yes (available) | — |
| Shell | `ParaMeshHollowCommand` | `MeshShellFeatures 🧪` | yes (available) | yes |
| Unisci | `ParaMeshCombineCommand` | `MeshCombineFeatures 🧪` | yes (available) | yes |
| Uniforme | `ParaMeshSmoothCommand` | `MeshSmoothFeatures 🧪` | yes (available) | yes |
| Boundary uniforme | `ParaMeshSmoothBoundaryCommand` | — | yes (available) | — |
| Inverti normale | `ParaMeshReverseNormalsCommand` | `MeshReverseNormalFeatures 🧪` | yes (available) | yes |
| Chiudi crepe | `ParaMeshCloseCracksCommand` | — | yes (available) | — |
| Cancella e Riempi | `ParaMeshEraseAndFillCommand` | — | yes (available) | — |
| Ponte | `ParaMeshBridgeCommand` | — | yes (available) | — |
| Allineamento mesh | `ParaMeshAlignCommand` | — | yes (available) | — |
| Attrarre a riferimento | `ParaMeshAttractToReferenceCommand` | — | yes (available) | — |
| Estrusione texture | `ParaMeshTextureCommand` | — | yes (available) | — |
| Separa | `ParaMeshExtractCommand` | `MeshSeparateFeatures 🧪` | yes (available) | yes |
| Scala mesh | `ParaMeshScaleCommand` | — | yes (available) | — |
| Rimuovi | `ParaMeshRemoveCommand` | `MeshRemoveFeatures 🧪` | yes (available) | yes |
| Converti mesh | `ParaMeshConvertCommand` | `MeshConvertFeatures 🧪` | yes (available) | yes |
| Converti in mesh quadrangolare | `ParaMeshToQuadMeshCommand` | — | yes (available) | — |
| Tavolozza mesh | `ParaMeshShowSelectionPanelCmd` | — | yes (available) | — |
| Stampa 3D | `ThreeDprintCmdDef` | `ExportManager` | yes (available) | yes |

## Design / FORMA tab (`FormTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Parallelepipedo | `TSplinePrimitiveBoxCommand` | `TSplineBodies.createBoxInput` | yes (available) | yes |
| Piano | `TSplinePrimitivePlaneCommand` | `TSplineBodies.createPlaneInput` | yes (available) | no |
| Cilindro | `TSplinePrimitiveCylinderCommand` | `TSplineBodies.createCylinderInput` | yes (available) | no |
| Sfera | `TSplinePrimitiveSphereCommand` | `TSplineBodies.createSphereInput` | yes (available) | yes |
| Toroide | `TSplinePrimitiveTorusCommand` | `TSplineBodies.createTorusInput` | yes (available) | no |
| Quadball | `TSplinePrimitiveQuadBallCommand` | `TSplineBodies.createQuadballInput` | yes (available) | yes |
| Tubo | `TSplinePrimitivePipe` | — | yes (available) | — |
| Faccia | `TSplineAppendFaceCommand` | — | yes (available) | — |
| Estrusione | `TSplineExtrudeCommand` | — | yes (available) | — |
| Rivoluzione | `TSplineRevolveCommand` | — | yes (available) | — |
| Sweep | `TSplineSweepCommand` | — | yes (available) | — |
| Loft | `TSplineLoft` | — | yes (available) | — |
| Modifica forma | `TSplineEditCommand` | — | yes (available) | — |
| Modifica in base a curva | `TSplineEditByCurveCmd` | — | yes (available) | — |
| Inserisci spigolo | `TSplineInsertEdgeCommand` | `FormFeature.insertEdge` | yes (available) | no |
| Suddividi | `TSplineSubsetCmd` | — | yes (available) | — |
| Inserisci punto | `TSplineInsertPointCommand` | — | yes (available) | — |
| Unisci bordo | `TSplineMergeEdgeCmd` | — | yes (available) | — |
| Ponte | `TSplineBridgeSubDCmd` | — | yes (available) | — |
| Riempi foro | `TSplineFillHoleCmd` | — | yes (available) | — |
| Cancella e Riempi | `TSplineEraseAndFillCmd` | — | yes (available) | — |
| Salda vertici | `TSplineWeldCommand` | — | yes (available) | — |
| Annulla saldatura spigoli | `TSplineUnWeldCommand` | — | yes (available) | — |
| Piega | `TSplineCreasedEdgeCommand` | — | yes (available) | — |
| Rimuovi piega | `TSplineUnCreaseEdgeCmd` | — | yes (available) | — |
| Smussa spigolo | `TSplineBevelEdgeCommand` | — | yes (available) | — |
| Scorri spigolo | `TSplineSlideEdgeCommand` | — | yes (available) | — |
| Uniforma | `TSplineSmoothCmd` | — | yes (available) | — |
| Rendi cilindrico | `TSplineCylindrifyCmd` | — | yes (available) | — |
| Trascina | `TSplinePullSubDCmd` | — | yes (available) | — |
| Livella | `TSplineFlattenSubDCmd` | — | yes (available) | — |
| Raddrizza | `TSplineStraightenCmd` | — | nesting: paid extension — to be verified | — |
| Accoppia | `TSplineMatchCmd` | — | yes (available) | — |
| Interpolazione | `TSplineInterpolateSubDCmd` | — | yes (available) | — |
| Ispessisci | `TSplineThickenCommand` | — | yes (available) | — |
| Congela | `TSplineFreezeCmd` | `FormFeatures` | yes (available) | yes |
| Scongela | `TSplineUnFreezeCmd` | `FormFeatures` | yes (available) | yes |
| Specchio - Interno | `TSplineInternalMirrorSymmetryCmd` | — | yes (available) | — |
| Circolare - Interno | `TSplineInternalCircularSymmetryCmd` | — | yes (available) | — |
| Specchio - Duplicato | `TSplineReflectionMirrorSymmetryCmd` | — | yes (available) | — |
| Circolare - Duplicato | `TSplineReflectionCircularSymmetryCmd` | — | yes (available) | — |
| Cancella simmetria | `TSplineClearSymmetryCommand` | — | yes (available) | — |
| Isola simmetria | `TSplineIsolateSymmetryCmd` | — | yes (available) | — |
| Modalità di visualizzazione | `TSplineToggleTessModeCmd` | `TSplineBody.displayMode` | yes (available) | no |
| Ripara corpo | `TSplineRepairBodyCmd` | — | yes (available) | — |
| Rendi uniforme | `TSplineMakeUniformCmd` | — | yes (available) | — |
| Migliora prestazioni | `TSplineCapSettingCommand` | — | yes (available) | — |
| Termina forma | `TSplineBaseFeatureStop` | `FormFeature.finishEdit` | yes (available) | yes |

## Design / LAMIERA tab (`SheetMetalTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Flangia (Base/Spigolo/Contornatura) | `FusionSheetMetalFlangeCommand` | `FlangeFeatures` | yes (available) | yes |
| Bordo | `FusionSheetMetalHemFlangeCommand` | `HemFeatures` | yes (available) | no |
| Tramoggia | `FusionSheetMetalLoftCommand` | `LoftedFlangeFeatures 🧪` | yes (available) | no |
| Piega | `SheetMetalFoldCmd` | `FoldFeatures 🧪` | yes (available) | no |
| Converti in lamiera | `ConvertToSheetMetalCmd` | `BRepBody.convertToSheetMetal` | yes (available) | yes |
| Converti in lamiera | `DMConvertToSheetMetalCmd` | `BRepBody.convertToSheetMetal` | yes (available) | yes |
| Crea modello piatto | `FusionSheetMetalFlatPatternCmd` | `FlatPattern` | yes (available) | no |
| Sviluppa | `FusionSheetmetalUnfoldCommand` | `UnfoldFeatures` | yes (available) | yes |
| Regole lamiera | `FusionSheetMetalRulesCommand` | `SheetMetalRules` | yes (available) | yes |
| Libreria di regole lamiera | `FusionSheetMetalRulesLibraryCommand` | `SheetMetalRules` | yes (available) | yes |
| Chiusura angolo | `FusionSheetMetalCornerCommand` | `CornerClosureFeatures 🧪` | yes (available) | no |
| Unisci per piega | `FusionJoinByBendCommand` | `JoinByBendFeatures 🧪` | yes (available) | no |
| Separazione | `FusionSheetMetalRipCommand` | `RipFeatures` | yes (available) | no |
| Riduzione | `FusionSheetMetalJogCommand` | — | yes (available) | — |
| Raccordo lamiera | `FusionSheetMetalFilletCommand` | `FilletFeatures` | yes (available) | yes |
| Smusso lamiera | `FusionSheetMetalChamferCommand` | `ChamferFeatures` | yes (available) | yes |
| Ripiega | `FusionSheetmetalRefoldCommand` | `RefoldFeatures` | yes (available) | yes |

## Design / PLASTICA tab (`PlasticTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Assegna regola plastica | `FusionAssignPlasticRuleCommand` | — | yes (available) | — |
| Gestisci regole plastica | `FusionManagePlasticRuleCommand` | `PlasticRules.addByCopy` | yes (available) | yes |
| Borchia | `FusionBossCommand` | `BossFeatures` | yes (available) | no |
| Accoppiamento a scatto | `FusionSnapFitCommand` | — | yes (available) | — |
| Bordo a incastro | `FusionLipCommand` | — | yes (available) | — |
| Appoggio | `FusionRestCommand` | — | yes (available) | — |
| Consigli di progettazione | `DesignAdviceCmd` | — | yes (available) | — |

## Design / ASSIEME tab (`AssemblyTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Distinta componenti | `MaterializedBomCmd` | — | bill of materials and releases (Manage): no | — |

## Design / GESTISCI tab (`ManageTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Assegna numero elemento | `PIMAssignItemNumberCmd` | — | bill of materials and releases (Manage): no | — |
| Rilascio rapido | `PIMQuickReleaseCmd` | — | bill of materials and releases (Manage): no | — |
| Rilascia con ordine di modifica | `PIMECOReleaseCmd` | — | bill of materials and releases (Manage): no | — |
| Plancia di comando | `PIMGoToDashboardCmd` | — | yes (available) | — |
| Dettagli | `PIMGoToItemDetailsCmd` | — | yes (available) | — |
| Ordini di modifica | `PIMGoToChangeOrderCmd` | — | bill of materials and releases (Manage): no | — |
| Nuova attività | `TaskManagementCreateTaskCmd` | — | yes (available) | — |
| Attività correlate | `TaskManagementRelatedTasksCmd` | — | yes (available) | — |
| Apri sul sito | `TaskManagementOpenTasksCmd` | — | yes (available) | — |

## Design / UTILITÀ tab (`ToolsTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Utensili di modellazione | `ModelingToggleCmdDef` | — | yes (available) | — |
| Preparazione nest | `MSFNestAuthoringCmd` | — | nesting: paid extension — to be verified | — |
| Script e moduli aggiuntivi... | `ScriptsManagerCommand` | `Application` | yes (available) | yes |
| Marketplace Design & Make | `ExchangeAppStoreCommand` | — | yes (available) | — |
| API di Fusion | `APIHelpCommand` | `Application` | yes (available) | yes |
| Gestisci libreria di filettature | `FusionManageThreadsLibraryCommand` | — | yes (available) | — |
| Nota foro/filettatura | `HoleThreadNoteCommand` | `PMIHoleThreadNotes.add 🧪` | yes (available) | yes |
| Nota | `LeaderLineNoteCommand` | `PMILeaderLineNotes.add 🧪` | yes (available) | yes |
| Dimensioni e quote | `DimensionNoteCommand` | — | yes (available) | — |
| Tolleranza geometrica | `GeometricToleranceNoteCommand` | — | yes (available) | — |
| Nota generale | `GeneralNoteCommand` | — | yes (available) | — |

## Design / AUTOMAZIONE tab (`AutomationTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| System Modeler | `FusionGraphExecutorAddinPaletteCmd` | — | yes (available) | — |
| System Modeler Documentation | `SystemModelerAutomationDocsCmd` | — | yes (available) | — |

## Design / PCB tab (`PCBTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Profilo PCB | `PCBDefineBoardCmd` | — | electronics: separate skill | — |
| Copia profilo EAGLE | `PCBImprintCmd` | — | electronics: separate skill | — |
| Modifica profilo EAGLE | `PCBBoardSketchEditCmd` | — | electronics: separate skill | — |
| Sposta componenti PCB | `PCBMoveComponentsCmd` | — | electronics: separate skill | — |
| Inverti componente | `PCBFlipComponentCmd` | — | electronics: separate skill | — |
| Stato PCB | `PCBStatusCmd` | — | electronics: separate skill | — |
| Termina PCB | `PCBStop` | — | electronics: separate skill | — |

## Design / Pacchetto tab (`Package3DTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Generatore pacchetti | `PackageGenerator` | — | electronics: separate skill | — |
| Generatore assiale | `cmd_id_Axial` | — | electronics: separate skill | — |
| Generatore BGA | `cmd_id_BGA` | — | electronics: separate skill | — |
| Generatore chip | `cmd_id_Chip` | — | electronics: separate skill | — |
| Generatore SOIC | `cmd_id_Soic` | — | electronics: separate skill | — |
| Generatore DFN-2 | `cmd_id_DFN2` | — | electronics: separate skill | — |
| Generatore DFN-3 | `cmd_id_DFN3` | — | electronics: separate skill | — |
| Generatore DFN-4 | `cmd_id_DFN4` | — | electronics: separate skill | — |
| Generatore connettore (maschio) con angolo a destra | `cmd_id_header_right_angle` | — | electronics: separate skill | — |
| Generatore connettore (femmina) con angolo a destra | `cmd_id_header_right_angle_socket` | — | electronics: separate skill | — |
| Generatore connettore (maschio) dritto | `cmd_id_header_straight` | — | electronics: separate skill | — |
| Generatore connettore (femmina) dritto | `cmd_id_header_straight_socket` | — | electronics: separate skill | — |
| Generatore SON | `cmd_id_Son` | — | electronics: separate skill | — |
| Generatore LED chip | `cmd_id_Chip_led` | — | electronics: separate skill | — |
| Generatore QFP | `cmd_id_Qfp` | — | electronics: separate skill | — |
| Generatore QFN | `cmd_id_Qfn` | — | electronics: separate skill | — |
| Serie di chip, generatore 2 lati convesso | `cmd_id_chiparray_2side_convex` | — | electronics: separate skill | — |
| Serie di chip, generatore 2 lati piatto/concavo | `cmd_id_chiparray_2side_flat_concave` | — | electronics: separate skill | — |
| Serie di chip, generatore 4 lati piatto/concavo | `cmd_id_chiparray_4side_flat` | — | electronics: separate skill | — |
| Generatore SOT143 | `cmd_id_sot143` | — | electronics: separate skill | — |
| Generatore SOT223 | `cmd_id_sot223` | — | electronics: separate skill | — |
| Generatore SOT23 | `cmd_id_sot23` | — | electronics: separate skill | — |
| Generatore SOTFL | `cmd_id_sotfl` | — | electronics: separate skill | — |
| Generatore PLCC | `cmd_id_Plcc` | — | electronics: separate skill | — |
| Generatore oscillatore a J | `cmd_id_Oscillator_j` | — | electronics: separate skill | — |
| Generatore oscillatore a l | `cmd_id_Oscillator_l` | — | electronics: separate skill | — |
| Generatore SOJ | `cmd_id_Soj` | — | electronics: separate skill | — |
| Generatore cristallo | `cmd_id_crystal` | — | electronics: separate skill | — |
| Generatore cristallo (HC49) | `cmd_id_crystal_hc49` | — | electronics: separate skill | — |
| Generatore DIP | `cmd_id_dip` | — | electronics: separate skill | — |
| Generatore calotta elettronica | `cmd_id_ecap` | — | electronics: separate skill | — |
| Generatore MELF | `cmd_id_Melf` | — | electronics: separate skill | — |
| Generatore stampato | `cmd_id_Molded` | — | electronics: separate skill | — |
| Generatore distanziale femmina | `cmd_id_female_standoff` | — | electronics: separate skill | — |
| Generatore distanziale maschio-femmina | `cmd_id_male_female_standoff` | — | electronics: separate skill | — |
| Generatore SOD | `cmd_id_Sod` | — | electronics: separate skill | — |
| Generatore blocco a innesto | `cmd_id_Snaplock` | — | electronics: separate skill | — |
| Generatore radiale | `cmd_id_Radial` | — | electronics: separate skill | — |
| Generatore LED circolare radiale | `cmd_id_Radial_Round_Led` | — | electronics: separate skill | — |
| Generatore concavo angolare | `cmd_id_Cornerconcave` | — | electronics: separate skill | — |
| Generatore SODFL | `cmd_id_Sodfl` | — | electronics: separate skill | — |
| Generatore A/DPAK | `cmd_id_TODPAK` | — | electronics: separate skill | — |
| Generatore diritto (femmina) connettore con montaggio su superficie | `cmd_id_surafce_mount_header_female` | — | electronics: separate skill | — |
| Generatore connettore (maschio) dritto con montaggio su superficie | `cmd_id_surface_mount_pin_header_male` | — | electronics: separate skill | — |
| Generatore connettore (maschio) con angolo retto e montaggio su superficie | `cmd_id_surface_mount_pin_header_male_right_angle` | — | electronics: separate skill | — |
| Generatore connettore DIP | `cmd_id_dip_socket` | — | electronics: separate skill | — |
| Generatore rettangolo con immersione radiale | `cmd_id_Radial_Dipped_Rectangle` | `SketchLines` | electronics: separate skill | yes |
| Fine | `Package3DStop` | — | electronics: separate skill | — |

## Design / SOLIDO tab (`BasefeatureSolidTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Termina lavorazione di base | `BaseFeatureStop` | `BaseFeatures` | yes (available) | yes |

## Design / SCHIZZO tab (`SketchTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Linea | `DrawPolyline` | `SketchLines` | yes (available) | yes |
| Linea punto medio | `SketchMidpointLine` | `SketchLines` | yes (available) | yes |
| Rettangolo mediante 2 punti | `ShapeRectangleTwoPoint` | `SketchLines` | yes (available) | yes |
| Rettangolo mediante 3 punti | `ShapeRectangleThreePoint` | `SketchLines` | yes (available) | yes |
| Rettangolo mediante centro | `ShapeRectangleCenter` | `SketchLines` | yes (available) | yes |
| Cerchio con centro-diametro | `CircleCenterRadius` | `SketchCircles` | yes (available) | yes |
| Cerchio mediante 2 punti | `CircleTwoPoint` | `SketchCircles` | yes (available) | yes |
| Cerchio mediante 3 punti | `CircleThreePoint` | `SketchCircles` | yes (available) | yes |
| Cerchio a 2 tangenti | `CircleTanTanRadius` | `SketchCircles` | yes (available) | yes |
| Cerchio mediante 3 tangenti | `CircleThreeTangent` | `SketchCircles` | yes (available) | yes |
| Arco a 3 punti | `ArcThreePoint` | `SketchArcs` | yes (available) | yes |
| Arco mediante centro e punto | `ArcCenterTwoPoint` | `SketchArcs` | yes (available) | yes |
| Arco tangente | `ArcTangent` | `SketchArcs` | yes (available) | yes |
| Poligono circoscritto | `ShapePolygonCircumscribed` | `SketchLines` | yes (available) | yes |
| Poligono inscritto | `ShapePolygonInscribed` | `SketchLines` | yes (available) | yes |
| Poligono da spigolo | `ShapePolygonEdge` | `SketchLines` | yes (available) | yes |
| Ellisse | `CircleElipse` | `SketchEllipses` | yes (available) | yes |
| Asola da centro a centro | `ShapeSlotCenterToCenter` | `SketchLines` | yes (available) | yes |
| Asola sull'intera lunghezza | `ShapeSlotOverall` | `SketchLines` | yes (available) | yes |
| Asola tramite punto centrale | `ShapeSlotCenterPoint` | `SketchLines` | yes (available) | yes |
| Asola dell'arco mediante tre punti | `ShapeArcSlotThreePoint` | `SketchArcs` | yes (available) | yes |
| Asola dell'arco mediante centro e punto | `ShapeArcSlotCenterTwoPoint` | `SketchArcs` | yes (available) | yes |
| Spline punto di adattamento | `DrawSpline` | `SketchFittedSplines` | yes (available) | yes |
| Spline punto di controllo | `DrawCVMSpline3D` | `SketchControlPointSplines` | yes (available) | no |
| Spline punto di controllo | `DrawCVMSpline5D` | `SketchControlPointSplines` | yes (available) | no |
| Curva conica | `ConicCurveCmd` | `SketchConicCurves` | yes (available) | no |
| Punto | `DrawPoint` | `SketchPoints` | yes (available) | no |
| Testo | `MTextCmd` | `SketchTexts` | yes (available) | yes |
| Adatta curve a sezione mesh | `FitCurvesToSectionCommand` | `Sketch` | yes (available) | no |
| Specchio | `MirrorSketchCommand` | `Sketch.mirror` | yes (available) | yes |
| Serie circolare | `CircularSketchPatternCommand` | — | yes (available) | — |
| Serie rettangolare | `RectangularSketchPatternCommand` | — | yes (available) | — |
| Proietta | `ProjectNewCmd` | `Sketch.project` | yes (available) | yes |
| Intersezione | `IntersectCmd` | `Sketch.intersectWithSketchPlane` | yes (available) | yes |
| Profilo di rotazione | `SpunProfileCmd` | `Sketch.createSpunProfile` | yes (available) | no |
| Includi geometria 3D | `Include3DGeometry` | `Sketch.include` | yes (available) | no |
| Proietta su superficie | `ProjectToSurface` | `Sketch.projectToSurface` | yes (available) | no |
| Curva di intersezione | `IntersectionCurve` | — | yes (available) | — |
| Curva isoparametrica | `SketchIsoparametricCurve` | — | yes (available) | — |
| Quota dello schizzo | `SketchDimension` | `SketchDimensions` | yes (available) | yes |
| Raccordo | `FilletSketchCmd` | `SketchArcs.addFillet` | yes (available) | yes |
| Uguale Distanza Smusso | `ChamferSketchEqualDistance` | `ChamferFeatures` | yes (available) | yes |
| Smusso angolo e distanza | `ChamferSketchDistanceAngle` | `ChamferFeatures` | yes (available) | yes |
| Due Distanza Smusso | `ChamferSketchDistanceDistance` | `ChamferFeatures` | yes (available) | yes |
| Curva di raccordo diffuso | `BlendG1CurveSketchCmd` | `SketchFittedSplines.addBlendCurve` | yes (available) | no |
| Offset | `Offset` | `Sketch.offset` | yes (available) | yes |
| Ritaglia | `TrimSketchCmd` | `SketchCurve.trim` | yes (available) | no |
| Estendi | `ExtendSketchCmd` | `SketchCurve.extend` | yes (available) | yes |
| Interrompi | `BreakSketchCmd` | `SketchCurve.breakCurve` | yes (available) | no |
| Scala schizzo | `SketchScaleCmd` | `Sketch.scale` | yes (available) | yes |
| AutoConstrain | `SketchAutoConstraintAndDimCmd` | — | AutoConstrain: no (tested) | — |
| AutoConstrain da riferimento | `SketchAutoConstraintAndDimFromDatumCmd` | — | AutoConstrain: no (tested) | — |
| Orizzontale/Verticale | `ConstraintHorizontalVertical` | `GeometricConstraints` | yes (available) | yes |
| Coincidente | `ConstraintCoincident` | `GeometricConstraints` | yes (available) | yes |
| Tangente | `ConstraintTangent` | `GeometricConstraints` | yes (available) | yes |
| Uguale | `ConstraintEqual` | `GeometricConstraints` | yes (available) | yes |
| Parallelo | `ConstraintParallel` | `GeometricConstraints` | yes (available) | yes |
| Perpendicolare | `ConstraintPerpendicular` | `GeometricConstraints` | yes (available) | yes |
| Fisso/mobile | `ConstraintFix` | `GeometricConstraints` | yes (available) | yes |
| PuntoMedio | `ConstraintMidPoint` | `GeometricConstraints` | yes (available) | yes |
| Concentrico | `ConstraintConcentric` | `GeometricConstraints` | yes (available) | yes |
| Collineare | `ConstraintCollinear` | `GeometricConstraints` | yes (available) | yes |
| Simmetria | `ConstraintSymmetry` | `GeometricConstraints` | yes (available) | yes |
| Curvatura | `ConstraintSmooth` | `GeometricConstraints` | yes (available) | yes |
| Poligono | `SketchPolygonConstraintCmd` | `SketchLines` | yes (available) | yes |
| Termina schizzo | `SketchStop` | `Sketch` | yes (available) | no |
| Termina con AutoConstrain | `SketchAutoConstrainAndFinish` | — | AutoConstrain: no (tested) | — |

## Design / POSIZIONE tab (`EditSnapshotTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Termina posizione | `SnapshotEditAccept` | `Snapshots` | yes (available) | no |
| Annulla posizione | `SnapshotEditCancel` | `Snapshots` | yes (available) | no |

## Design / Modifica diretta della mesh tab (`ParaMeshBaseFeatureTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Termina modifica diretta | `ParaMeshBaseFeatureStopCommand` | `BaseFeature.finishEdit` | yes (available) | yes |

## Design / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Ripeti... | `RepeatCommand` | — | yes (available) | — |
| Ripeti | `RedoCommand` | — | yes (available) | — |
| Annulla | `UndoCommand` | — | yes (available) | — |
| Panoramica | `PanCommand` | `Viewport.camera` | yes (available) | yes |
| Zoom | `ZoomCommand` | `Viewport.camera` | yes (available) | yes |
| Orbita vincolata | `ConstrainedOrbitCommand` | `Viewport.camera` | yes (available) | yes |
| Imposta centro dell'orbita | `SetOrbitCenterCommand` | `Viewport.camera` | yes (available) | yes |
| Ripristina centro dell'orbita | `ResetOrbitCenterCommand` | `Viewport.camera` | yes (available) | yes |
| Allinea componenti | `AlignComponentsCmd` | — | yes (available) | — |
| Allinea | `AlignGeometryCmd` | — | yes (available) | — |
| Aggiorna modello piatto | `UpdateFlatPatternCommand` | `FlatPattern` | yes (available) | no |
| Modifica diretta | `BeginEditInPlaceCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Modifica riferimento assieme | `BeginEIPAsEditContextCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza riferimento assieme | `ContextUpdateFromParentCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Termina Modifica diretta | `EndEditInPlaceCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Attiva | `FusionActivateLocalCompCmd` | `Occurrence.activate` | yes (available) | yes |
| Attiva riferimento assieme | `EIPContextActivateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Interrompi collegamento | `EIPContextBreakLinkCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza riferimento assieme | `EIPContextUpdateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza tutti i riferimenti assieme | `EIPContextsUpdateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza tutti i riferimenti assieme | `ContextUpdateAllFromParentCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Attiva | `FusionSheetMetalFlatPatternActivateCmd` | `FlatPattern` | yes (available) | no |
| Aggiorna modello piatto | `UpdateFlatPatternFromMainDesignCommand` | `FlatPattern` | yes (available) | no |
| Aggiorna tutti i modelli piatti | `UpdateAllFlatPatternsCommand` | `FlatPattern` | yes (available) | no |
| Blocca | `FusionGroundComponentsCommand` | `Occurrence.isGrounded` | yes (available) | yes |
| Sblocca | `FusionUnGroundComponentsCommand` | `Occurrence.isGrounded` | yes (available) | yes |
| Fissa a principale | `GroundToParentCommand` | `Occurrence.isGroundToParent` | yes (available) | no |
| Svincolato da principale | `UnGroundToParentCommand` | `Occurrence.isGroundToParent` | yes (available) | no |
| Rendi rigido | `RigidSubAssemblyCommand` | — | yes (available) | — |
| Rendi flessibile | `FlexibleSubAssemblyCommand` | — | yes (available) | — |
| Modifica lavorazione  | `FusionDcMoveBodyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcMoveCopyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica della posizione iniziale  | `FusionDcEditInitialPositionCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica della posizione iniziale  | `FusionEditInitialPositionCommand` | `Occurrence.initialTransform` | yes (available) | no |
| Modifica lavorazione  | `FusionDcAlignEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Sposta nel gruppo | `FusionMoveToSurfaceGroupCommand` | `MoveFeatures` | yes (available) | yes |
| Sposta nel gruppo | `FusionMoveToWorkGeometryCustomGroupCommand` | `MoveFeatures` | yes (available) | yes |
| Sposta nel gruppo | `FusionMoveToSketchCustomGroupCommand` | `MoveFeatures` | yes (available) | yes |
| Cambia configurazione | `FusionComponentChangeConfigCommand` | — | configurations: no | — |
| Crea componenti dai corpi | `FusionCreateNewCompCmdFromBody` | `BRepBody.createComponent` | yes (available) | yes |
| Nuovo componente | `FusionCreateNewCompCmdFromSel` | `Occurrences.addNewComponent` | yes (available) | yes |
| Modifica lavorazione  | `FusionCreateComponentFromBodyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Crea disegno | `FusionDrawingCreateFromComponentsCommand` | `DrawingManager.createDrawing 🧪` | yes (available) | no |
| Nuovo gruppo | `FusionCreateSurfaceGroupCommand` | — | yes (available) | — |
| Nuovo gruppo di schizzi | `FusionCreateSketchCustomGroupCommand` | — | yes (available) | — |
| Nuovo gruppo | `FusionCreateWorkGeometryCustomGroupCommand` | — | yes (available) | — |
| Crea gruppo di selezione | `CreateSelectionGroupCmd` | `Selections` | yes (available) | no |
| Modifica schizzo | `SketchActivate` | `Sketches.itemByName` | yes (available) | yes |
| Ridefinsci piano dello schizzo | `SketchRedefineCommand` | `Sketch.redefine` | yes (available) | no |
| Seleziona piano dello schizzo | `SelectSketchPlaneCommand` | `Selections` | yes (available) | no |
| Gestisci proiezioni perse | `SketchRelinkProjectionCmd` | — | yes (available) | — |
| Modifica lavorazione  | `FusionDcEditCanvasCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Calibra | `FusionDcCalibrateCanvasCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `FusionDcEditDecalCommand` | `Decals` | yes (available) | no |
| Modifica raccordo | `FusionFilletEditCommand` | `FilletFeatures` | yes (available) | yes |
| Modifica smusso | `FusionChamferEditCommand` | `ChamferFeatures` | yes (available) | yes |
| Modifica foro | `FusionHoleEditCommand` | `HoleFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcHoleEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| DcBoltConnEdit | `DcBoltConnEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionLoftEditCommand` | `LoftFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceLoftEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcRibEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica filettatura | `FusionThreadEditCommand` | `ThreadFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcThreadEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie circolare | `PatternCircularEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie rettangolare | `PatternRectangularEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie circolare | `FusionDcCircularPatternEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcComplexPatternEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie su traiettoria | `FusionDcPathPatternEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie rettangolare | `FusionDcRectangularPatternEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcMirrorPatternEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica serie su traiettoria | `PatternOnPathEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcDraftEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `FusionDcEmbossEditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica tubo | `TSplinePipeEditCommand` | `FormFeatures` | yes (available) | yes |
| Modifica corrispondenza | `TSplineMatchEditCmd` | `FormFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfacePatchEditCommand` | `PatchFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceStitchEditCommand` | `StitchFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceUnStitchEditCommand` | `UnstitchFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcSurfaceDeleteFaceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcReverseNormalEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSurfaceOffsetEditCommand` | `OffsetFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcSurfaceOffsetShellEditCommand` | `OffsetFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcMidSurfaceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSurfaceShellEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSurfaceTrimEditCommand` | `TrimFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcSurfaceUntrimEditCommand` | `UntrimFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcSurfaceExtendEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSurfaceRuledEditCommand` | `RuledSurfaceFeatures` | yes (available) | no |
| Modifica lavorazione  | `FusionDcWebEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcScaleEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `DcReplaceWithPrimitiveEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica Rimuovi facce | `FusionRemoveFacesEditCommand` | `RemoveFeatures` | yes (available) | no |
| Modifica Rimuovi lavorazioni | `FusionRemoveFeaturesEditCommand` | `RemoveFeatures` | yes (available) | no |
| Modifica lavorazione  | `DCFusionGapFillEditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Taglia schizzo | `SliceSketchCommand` | `Sketch.isModelSliced` | yes (available) | no |
| Elimina suddivisioni schizzo | `UnsliceSketchCommand` | `Sketch.isModelSliced` | yes (available) | no |
| Abilita controllo completamente vincolato | `EnableFullyConstrained` | `Sketch.isFullyConstrained` | yes (available) | yes |
| Disabilita controllo completamente vincolato | `DisableFullyConstrained` | — | yes (available) | — |
| Modifica serie circolare | `SketchPatternCircularEdit` | `Sketch` | yes (available) | no |
| Modifica serie rettangolare | `SketchRectangularPatternEdit` | `RectangularPatternFeatures` | yes (available) | yes |
| Interrompi collegamento | `SketchUnProjectCmd` | `Sketch` | yes (available) | no |
| Modifica testo | `EditTextCmd` | `SketchText.text` | yes (available) | yes |
| Modifica testo | `EditMTextCmd` | `SketchTexts` | yes (available) | yes |
| Esplodi testo | `ExplodeTextCmd` | `SketchText.explode` | yes (available) | no |
| Normale/Costruzione | `SketchConstructionCmd` | `SketchCurve.isConstruction` | yes (available) | yes |
| Normale/Linea d'asse | `SketchCenterLineCmd` | `SketchLine.isCenterLine` | yes (available) | yes |
| Testo su percorso | `TextOnPathCmd` | `AlongPathTextDefinition` | yes (available) | no |
| Modifica curva isoparametrica | `Include3DIsoParamCurveCmdEdit` | `Sketch` | yes (available) | no |
| Modifica lavorazione | `DcBossEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `DcSnapFitEdit` | — | yes (available) | — |
| Modifica lavorazione | `DcRestEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `DcLipEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Fisso/mobile | `SketchFixConstraintCmd` | `SketchCurve.isFixed` | yes (available) | no |
| Elimina coincidenti | `DeleteCoincidentConstraintCmd` | — | yes (available) | — |
| Spostare nel piano dello schizzo | `SketchConstrainOnPlaneCmd` | — | yes (available) | — |
| Salva schizzo con nome | `SaveSketchAsDWG` | `Documents.add` | yes (available) | yes |
| Apri/Chiudi curva di spline | `SplineCloseCurve` | `SketchFittedSplines` | yes (available) | yes |
| Inserisci punto di adattamento spline | `SplineInsertPoint` | `SketchFittedSplines` | yes (available) | yes |
| Inserisci punto di controllo spline | `InsertControlPoint` | — | yes (available) | — |
| Visualizza riquadro di controllo | `InsertControlPolygon` | `SketchLines` | yes (available) | yes |
| Attiva maniglia tangente | `AddTangentHandle` | `SketchFittedSpline.activateTangentHandle` | yes (available) | no |
| Attiva maniglia di curvatura | `AddCurvatureHandle` | `SketchFittedSpline.activateCurvatureHandle` | yes (available) | no |
| Disattiva maniglia di curvatura | `DeleteCurvatureCommand` | — | yes (available) | — |
| Disattiva maniglia tangente | `DeleteTangentCommand` | — | yes (available) | — |
| Attiva/disattiva la visualizzazione della curvatura | `FusionToggleSetupCurveCurvatureCombCommand` | `CurvatureCombAnalyses` | yes (available) | no |
| Imposta visualizzazione curvatura | `FusionCurveCurvatureCombSetupCommand` | `CurvatureCombAnalyses` | yes (available) | no |
| Modifica PMI | `EditHoleThreadNoteCommand` | `PMIHoleThreadNote 🧪` | yes (available) | no |
| Modifica lavorazione | `DMEditHoleThreadNoteCommand` | — | yes (available) | — |
| Converti in PMI Fusion | `ConvertImportedPMICommand` | `Documents.add` | yes (available) | yes |
| Contrassegna come aggiornato | `ResetPMIStateCommand` | — | yes (available) | — |
| Mostra PMI importato | `DisplayImportedPMICommand` | `Viewport.camera` | yes (available) | yes |
| Modifica PMI | `EditLeaderLineNoteCommand` | `PMILeaderLineNote 🧪` | yes (available) | no |
| Modifica annotazione | `DMEditLeaderLineNoteCommand` | — | yes (available) | — |
| Modifica PMI | `EditDimensionNoteCommand` | — | yes (available) | — |
| Modifica annotazione | `DMEditDimensionNoteCommand` | — | yes (available) | — |
| Modifica PMI | `EditGeometricToleranceNoteCommand` | — | yes (available) | — |
| Modifica annotazione | `DMEditGeometricToleranceNoteCommand` | — | yes (available) | — |
| Modifica giunto  | `EditJointAssembleCmd` | `Joint.jointMotion` | yes (available) | yes |
| Modifica giunto  | `DcEditJointAssembleCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica giunto  | `DcEditJointAsBuiltCmd` | `AsBuiltJoints` | yes (available) | yes |
| Modifica vincolo | `DcEditAssemblyMateCmd` | `Joints` | yes (available) | yes |
| Modifica vincolo | `EditAssemblyMateCmd` | `Joints` | yes (available) | yes |
| Modifica limiti movimento | `EditJointDOFLimitsCmd` | `JointLimits` | yes (available) | no |
| Modifica limiti offset | `EditOffsetLimitsCmd` | — | yes (available) | — |
| Modifica gruppo rigido  | `DcEditRigidGroupCmd` | `RigidGroups` | yes (available) | yes |
| Modifica gruppo rigido  | `EditRigidGroupCmd` | `RigidGroups` | yes (available) | yes |
| Blocca movimento | `LockJointDOFCmd` | `Joint.isLocked` | yes (available) | no |
| Sblocca movimento | `UnlockJointDOFCmd` | `Joint.isLocked` | yes (available) | no |
| Blocca movimento | `LockJointCmd` | `Joint.isLocked` | yes (available) | no |
| Sblocca movimento | `UnlockJointCmd` | `Joint.isLocked` | yes (available) | no |
| Sopprimi | `SuppressJointOccurrenceCmd` | `Joint.isSuppressed` | yes (available) | yes |
| Scopri | `UnsuppressJointOccurrenceCmd` | `Joint.isSuppressed` | yes (available) | yes |
| Sopprimi | `SuppressTransitionalRelationshipOccurrenceCmd` | — | yes (available) | — |
| Scopri | `UnsuppressTransitionalRelationshipOccurrenceCmd` | — | yes (available) | — |
| Sopprimi | `SuppressGeometricRelationshipOccurrenceCmd` | — | yes (available) | — |
| Scopri | `UnsuppressGeometricRelationshipOccurrenceCmd` | — | yes (available) | — |
| Sopprimi vincolo | `SuppressConstraintCmd` | `AssemblyConstraint.isSuppressed 🧪` | yes (available) | yes |
| Scopri vincolo | `UnSuppressConstraintCmd` | `AssemblyConstraint.isSuppressed 🧪` | yes (available) | yes |
| Sopprimi | `SuppressRigidGroupCmd` | `RigidGroups` | yes (available) | yes |
| Scopri | `UnsuppressRigidGroupCmd` | `RigidGroups` | yes (available) | yes |
| Anima giunto | `AnimateJointCmd` | — | yes (available) | — |
| Anima relazioni giunto | `AnimateModelCmd` | — | yes (available) | — |
| Crea versione | `CreateVersionCommandFromCtxMenu` | `Document.save` | yes (available) | yes |
| Vai all'inizio | `RestoreJointCmd` | — | yes (available) | — |
| Imposta come posizione iniziale | `RedefineJointHomeCmd` | — | yes (available) | — |
| Modifica relazione tangente | `EditTransitionalRelationshipCmd` | — | yes (available) | — |
| Modifica relazione tangente | `DcEditTransitionalRelationshipCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica | `EditMotionRelationshipCmd` | `MotionLinks` | yes (available) | no |
| Modifica lavorazione | `DcEditMotionRelationshipCmd` | `MotionLinks` | yes (available) | no |
| Sopprimi | `SuppressMotionRelationshipCmd` | `MotionLinks` | yes (available) | no |
| Scopri | `UnsuppressMotionRelationshipCmd` | `MotionLinks` | yes (available) | no |
| Seleziona componenti | `SelectComponentsCmd` | `Selections` | yes (available) | no |
| Seleziona componenti | `SelectTransRelComponentsCmd` | `Selections` | yes (available) | no |
| Seleziona giunti collegati | `SelectMotionLinkJointsCmd` | `Selections` | yes (available) | no |
| Modifica | `EditMotionStudyCmd` | `MotionLinks` | yes (available) | no |
| Modifica origine giunto  | `EditJointOriginCmd` | `JointOrigins` | yes (available) | yes |
| Modifica origine giunto  | `EditJointOriginR2Cmd` | `JointOrigins` | yes (available) | yes |
| Modifica sistema di coordinate utente (UCS) | `EditCoordinateSystemR2Cmd` | `ConstructionPlanes` | yes (available) | yes |
| Modifica | `EditContactSetCmd` | `ContactSets` | yes (available) | no |
| Sopprimi | `SuppressContactSetCmd` | `ContactSets` | yes (available) | no |
| Scopri | `UnsuppressContactSetCmd` | `ContactSets` | yes (available) | no |
| Mostra/Nascondi corpi associati | `GhostedBodyToggleCommand` | — | yes (available) | no |
| Modifica area grafica | `FusionEditCanvasCommand` | `Canvas.transform` | yes (available) | yes |
| Calibra | `FusionCalibrateCanvasCommand` | `Canvas.transform` | yes (available) | yes |
| Sostituire file di immagine dell'area grafica | `FusionReplaceCanvasImageCommand` | — | yes (available) | — |
| Modifica decalcomania | `FusionEditDecalCommand` | `Decals` | yes (available) | no |
| Sostituisci file di immagine | `FusionReplaceDecalImageCommand` | `Decals` | yes (available) | no |
| Modifica | `FusionEditCurvatureCombAnalysisCommand` | `CurvatureCombAnalyses` | yes (available) | no |
| Modifica | `FusionEditZebraAnalysisCommand` | `ZebraAnalyses` | yes (available) | no |
| Modifica | `FusionEditEnvironmentMapAnalysisCommand` | `EnvironmentMapAnalyses` | yes (available) | no |
| Modifica | `FusionEditDraftAnalysisCommand` | `DraftAnalyses` | yes (available) | yes |
| Modifica | `FusionEditCurvatureMapAnalysisCommand` | `CurvatureMapAnalyses` | yes (available) | no |
| Modifica | `FusionEditAccessibilityAnalysisCommand` | `AccessibilityAnalyses` | yes (available) | yes |
| Modifica | `FusionEditHalfSectionViewCommand` | `SectionAnalyses` | yes (available) | yes |
| Modifica | `FusionEditCenterOfMassCommand` | `PhysicalProperties` | yes (available) | yes |
| Modifica | `FusionEditMinimumRadiusAnalysisCommand` | `MinimumRadiusAnalyses` | yes (available) | yes |
| Modifica | `FusionEditIsoCurveAnalysisCommand` | `IsoCurveAnalyses` | yes (available) | no |
| Modifica analisi pila elementi di fissaggio | `FusionEditFastenerStackAnalysisCommand` | — | yes (available) | — |
| Nuova vista con nome | `AddNamedViewCommand` | `Viewport.camera` | yes (available) | yes |
| Elimina | `RemoveNamedViewCommand` | `RemoveFeatures` | yes (available) | no |
| Aggiorna vista con nome | `UpdateNamedViewCameraCommand` | `Viewport.camera` | yes (available) | yes |
| Nuova luce | `AddNamedLightCommand` | `Lights 🧪` | yes (available) | no |
| Modifica luce | `FusionEditNamedLightCommand` | `Lights 🧪` | yes (available) | no |
| Assegna regola plastica | `FusionSwitchPlasticRuleCommand` | — | yes (available) | — |
| Rimuovi regola plastica | `FusionRemovePlasticRuleCommand` | `RemoveFeatures` | yes (available) | no |
| Dissolvi lavorazioni | `DissolveFeaturesCmdDef` | — | yes (available) | — |
| Rendi indipendente | `FusionMakeIndependentCommand` | — | yes (available) | — |
| Selezionare i giunti di riferimento | `SelectJointsByComponentCmd` | `Selections` | yes (available) | no |
| Rimuovi sostituzione aspetto | `FusionRemoveOverrideCommand` | `RemoveFeatures` | yes (available) | no |
| Proprietà | `FusionPropertiesCommand` | — | yes (available) | — |
| Risolvi componente | `FusionResolveMissingXRefCmd` | — | yes (available) | — |
| Sola lettura per utente corrente | `EnableReadOnlyCmd` | — | yes (available) | — |
| Sola lettura per utente corrente | `DisableReadOnlyCmd` | — | yes (available) | — |
| FlatMeshShadingCmd | `FlatMeshShadingCmd` | — | yes (available) | — |
| SmoothMeshShadingCmd | `SmoothMeshShadingCmd` | — | yes (available) | — |
| MeshTriangulateCommand | `MeshTriangulateCommand` | — | yes (available) | — |
| FusionInsertComponentCommand | `FusionInsertComponentCommand` | `Occurrences.addByInsert` | yes (available) | yes |
| Esporta... | `FusionExportComponentCommand` | `Documents.add` | yes (available) | yes |
| Esporta serie piatta | `ExportFlatPatternCmd` | `FlatPattern` | yes (available) | no |
| Salva copia con nome | `FusionSaveAsComponentCommand` | `Documents.add` | yes (available) | yes |
| Salva progettazione configurata con nome | `FusionSaveAsConfiguredDesignCommand` | `Documents.add` | configurations: no | yes |
| Salva configurazione con nome | `FusionSaveAsConfigurationCommand` | `Documents.add` | configurations: no | yes |
| Salva configurazione con nome | `FusionCDSaveAsConfigurationCommand` | `Documents.add` | configurations: no | yes |
| Salva con nome e sostituisci | `FusionSaveAsAndReplaceComponentCommand` | `Documents.add` | yes (available) | yes |
| Salva come più recente | `PLM360SaveAsLatestCommand` | `Documents.add` | yes (available) | yes |
| Salva come mesh | `FusionSaveAsSTLCommand` | `Documents.add` | yes (available) | yes |
| Salva in formato OBJ | `FusionSaveAsOBJCommand` | `Documents.add` | yes (available) | yes |
| Salva riquadro di controllo come OBJ | `FusionSaveControlFrameAsOBJCommand` | `Documents.add` | yes (available) | yes |
| Salva T-spline come IGA | `TSplineSaveAsIGACommand` | `FormFeatures` | yes (available) | yes |
| Apri | `PLM360OpenAttachmentCommand` | `Documents.add` | yes (available) | yes |
| Open Source | `OpenDeriveDocumentCommand` | `Documents.add` | yes (available) | yes |
| Carica versione più recente | `PLM360RefreshDocumentCommand` | `Documents.add` | yes (available) | yes |
| Carica versione più recente | `GetLatestCmd` | `DocumentReference.getLatestVersion` | yes (available) | yes |
| Carica ultima versione del traguardo | `GetLatestMilestoneCmd` | — | yes (available) | — |
| Aggiorna riferimenti esterni | `GetAllLatestCmd` | `DocumentReference.getLatestVersion` | yes (available) | yes |
| Carica tutte le versioni più recenti | `UpdateAllLatestCmd` | `DocumentReference.getLatestVersion` | yes (available) | yes |
| Mostra in posizione | `ShowInLocationCmd` | — | yes (available) | no |
| Fai avanzare a più recente | `AdvanceToLatestCmd` | — | yes (available) | — |
| Cronologia | `ShowHistoryCmd` | — | yes (available) | no |
| Interrompi collegamento | `BreakXRefLinkCmd` | `Occurrence.breakLink` | yes (available) | no |
| Sostituisci componente | `FusionComponentReplaceCommand` | `Occurrence.replace` | yes (available) | yes |
| Copia | `CopyCommand` | `BRepBody.copyToComponent` | yes (available) | no |
| Taglia | `CutCommand` | — | yes (available) | — |
| Incolla | `PasteCommand` | `Occurrences.addNewComponentCopy` | yes (available) | no |
| Incolla nuovo | `FusionPasteNewCommand` | `Documents.add` | yes (available) | yes |
| Esporta DXF | `SketchExportToDXFCommand` | `Documents.add` | yes (available) | yes |
| Elimina tutte le lavorazioni da Contrassegno cronologia | `FusionTrimFeaturesCommand` | `TrimFeatures` | yes (available) | no |
| SurfaceShellDeleteCommand | `SurfaceShellDeleteCommand` | `ShellFeatures` | yes (available) | yes |
| Rinomina | `RenameBrowserCmd` | `Component.name` | yes (available) | yes |
| Vista su faccia o piano | `LookAtCommand` | `Viewport.camera` | yes (available) | yes |
| Controllo dettaglio visualizzazione | `TessellationControlCmd` | — | yes (available) | — |
| Mostra profilo | `ShowProfile` | — | yes (available) | no |
| Nascondi profilo | `HideProfile` | — | yes (available) | no |
| Mostra quota | `ShowDimension` | — | yes (available) | no |
| Nascondi quote | `HideDimension` | — | yes (available) | no |
| Mostra geometrie proiettate | `ShowProjectedGeometries` | — | yes (available) | no |
| Nascondi geometrie proiettate | `HideProjectedGeometries` | — | yes (available) | no |
| Mostra geometrie di costruzione | `ShowConstructionGeometries` | — | yes (available) | no |
| Nascondi geometrie di costruzione | `HideConstructionGeometries` | — | yes (available) | no |
| Mostra/Nascondi | `VisibilityToggleCmd` | `Occurrence.isLightBulbOn` | yes (available) | yes |
| Mostra tutti i componenti | `ShowAllComponentsCmd` | — | yes (available) | no |
| Mostra tutti i corpi | `ShowAllBodiesCmd` | — | yes (available) | no |
| Mostra tutto | `ShowAllGroupMembersCmd` | — | yes (available) | no |
| Selezionabile/Non selezionabile | `SelectabilityToggleCmd` | `Selections` | yes (available) | no |
| Mostra/Nascondi piani | `PlanesVisibilityToggleCmd` | — | yes (available) | no |
| Mostra/Nascondi assi | `AxesVisibilityToggleCmd` | — | yes (available) | no |
| Mostra/Nascondi punti | `PointsVisibilityToggleCmd` | — | yes (available) | no |
| Controllo dell'opacità | `OpacityControlCmd` | `Occurrence.visibleOpacity` | yes (available) | yes |
| Opacità personalizzata | `CustomOpacityControlCmd` | `CustomFeatures 🧪` | yes (available) | no |
| 10% | `OpacityCtrlTenCmd` | — | yes (available) | — |
| 20% | `OpacityCtrlTwentyCmd` | — | yes (available) | — |
| 30% | `OpacityCtrlThirtyCmd` | — | yes (available) | — |
| 40% | `OpacityCtrlFortyCmd` | — | yes (available) | — |
| 50% | `OpacityCtrlFiftyCmd` | — | yes (available) | — |
| 60% | `OpacityCtrlSixtyCmd` | — | yes (available) | — |
| 70% | `OpacityCtrlSeventyCmd` | — | yes (available) | — |
| 80% | `OpacityCtrlEightyCmd` | — | yes (available) | — |
| 90% | `OpacityCtrlNinetyCmd` | — | yes (available) | — |
| 100% | `OpacityCtrlHundredCmd` | — | yes (available) | — |
| Isola | `IsolateCmd` | `Occurrence.isIsolated` | yes (available) | yes |
| Rimuovi isolamento | `UnisolateCmd` | `Occurrence.isIsolated` | yes (available) | yes |
| Rimuovi isolamento per tutti | `UnisolateAllCmd` | `Occurrence.isIsolated` | yes (available) | yes |
| Colore componente ciclo | `CycleComponentColorCmd` | — | yes (available) | — |
| Trova nel browser | `FindInBrowser` | — | yes (available) | — |
| Trova nella finestra | `FindInWindow` | — | nesting: paid extension — to be verified | — |
| Trova nella timeline | `FusionFindInTimeline` | — | yes (available) | — |
| Passare a Modellazione parametrica | `ConvertToPMDesignCommand` | `Design.designType` | yes (available) | yes |
| Passa a Modellazione diretta | `ConvertToDMDesignCommand` | `Design.designType` | yes (available) | yes |
| SelectiveCreateWorkingModelFromBodyCommand | `SelectiveCreateWorkingModelFromBodyCommand` | `Selections` | yes (available) | no |
| SelectiveCreateWorkingModelFromCompCommand | `SelectiveCreateWorkingModelFromCompCommand` | `Selections` | yes (available) | no |
| Ignora/Mostra problemi della pila | `FastenerStackAnalysisIgnoreToggleCmd` | — | yes (available) | no |
| Inserisci elemento di fissaggio simile | `FastenersInsertSimilar` | — | yes (available) | — |
| Modifica elemento di fissaggio | `FastenersEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Sostituisci elemento di fissaggio | `FastenersReplaceCommand` | — | yes (available) | — |
| Risolvi elemento di fissaggio | `ResolveFastenerCommand` | — | yes (available) | — |
| Aggiorna automaticamente dimensioni | `FastenersStackUpdateCmd` | `FastenerOccurrenceDefinition.updateSize 🧪` | yes (available) | no |
| Opzioni elementi di fissaggio | `FastenersOptionsCmd` | — | yes (available) | — |
| Aggiorna automaticamente tutte le dimensioni | `FastenersAllStacksUpdateCmd` | `FastenerOccurrenceDefinition.updateSize 🧪` | yes (available) | no |
| Modifica disposizione | `DcArrangeEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica disposizione | `DcAdvandedArrangeEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica area di disegno | `DcArrangeEditSketchCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica solido di delimitazione | `DcStockModelEditCommand` | `BoxFeatures` | yes (available) | no |
| Modifica lavorazione | `FusionEditFeatureCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `FusionEditDcFeatureCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Dissolvi | `DissolveFeatureCmdDef` | — | yes (available) | — |
| Modifica lavorazione  | `FusionSculptEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `BoxPrimitiveEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `CylinderPrimitiveEditCommand` | `CylinderFeatures` | yes (available) | no |
| Modifica lavorazione | `SpherePrimitiveEditCommand` | `SphereFeatures` | yes (available) | no |
| Modifica lavorazione  | `TorusPrimitiveEditCommand` | `TorusFeatures` | yes (available) | no |
| Modifica lavorazione  | `PipePrimitiveEditCommand` | `PipeFeatures` | yes (available) | yes |
| Modifica lavorazione  | `CoilPrimitiveEditCommand` | `CoilFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcFilletEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSurfaceThickenEditCommand` | `ThickenFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcChamferEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcShellFeatureEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionExtrudeEditCommand` | `ExtrudeFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceExtrudeEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionRevolveEditCommand` | `RevolveFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceRevolveEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionSweepEditCommand` | `SweepFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionSurfaceSweepEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionCombineEditCommand` | `CombineFeatures` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSplitBodyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcSplitFaceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazioni | `FusionDcReplaceFaceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcDeleteFaceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionDcPartingLineSplitEditCommand` | `SilhouetteSplitFeatures` | yes (available) | no |
| Modifica piano di costruzione  | `FusionDcEditConstructionTangentPlaneCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione  | `FusionDcEditConstructionPlaneFromThreePointsCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione | `FusionDcEditConstructionPlanePerpendicularToPlaneCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisNormalToFaceCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromThreePlanesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromCircleOrSphereCommand` | `SketchCircles` | yes (available) | yes |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneByPlaneOffsetCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione | `FusionDcEditConstructionMidPlaneCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneFromTwoEdgesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione  | `FusionDcEditConstructionPlaneAtAngleCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneAlongPathCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromPointCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointAtEdgeAndPlaneCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointThroughTwoEdgesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica punto di costruzione | `FusionDcEditConstructionPointAlongPathCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisThroughCylinderCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisFromTwoPlanesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica asse di costruzione  | `FusionDcEditConstructionAxisThroughEdgeCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica asse di costruzione  | `FusionDcEditConstructionAxisThroughTwoPointsCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione  | `FusionOffsetFacesEditCommand` | `OffsetFacesFeatures` | yes (available) | yes |
| Modifica | `BaseFeatureActivate` | `BaseFeatures` | yes (available) | yes |
| Modifica | `SnapshotActivate` | `Viewport.camera` | yes (available) | yes |
| Modifica | `TSplineBaseFeatureActivate` | `FormFeatures` | yes (available) | yes |
| Modifica | `PCBActivate` | — | yes (available) | — |
| Modifica flangia | `FusionBaseFaceEditCommand` | `BaseFeatures` | yes (available) | yes |
| Modifica raccordo lamiera | `FusionSheetMetalFilletEditCommand` | `FilletFeatures` | yes (available) | yes |
| Modifica smusso lamiera | `FusionSheetMetalChamferEditCommand` | `ChamferFeatures` | yes (available) | yes |
| Modifica Chiusura angolo | `FusionCornerEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica Unisci per piega | `FusionJoinByBendEditCommand` | `JoinByBendFeatures 🧪` | yes (available) | no |
| Modifica Piega cosmetica | `FusionSheetMetalCosmeticBendEditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica riduzione | `FusionSheetMetalJogEditCommand` | — | yes (available) | — |
| Modifica profilo di schizzo | `FusionEditDcFeatureProfileCommand` | — | yes (available) | — |
| Modifica profilo di schizzo | `ProfileSketchActivate` | — | yes (available) | — |
| Modifica spiegatura | `SheetmetalEditUnfoldCommand` | `UnfoldFeatures` | yes (available) | yes |
| Modifica piega | `SheetMetalFoldEditCmd` | `FoldFeatures 🧪` | yes (available) | no |
| Modifica Converti in lamiera | `ConvertToSheetMetalEditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica separazione | `SheetMetalRipEditCmd` | `RipFeatures` | yes (available) | no |
| Modifica lavorazione | `APIFeatureEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione derivata | `EditDeriveCommand` | `DeriveFeatures` | yes (available) | yes |
| Interrompi collegamento | `BreakExternalDeriveLinkCmd` | `DeriveFeature.breakLink` | yes (available) | no |
| Modifica lavorazione  | `FusionAutomatedModelingEditCommand` | `TimelineObject.rollTo` | automated / generative modeling: no | yes |
| Configura | `ConfigureEntityCmd` | — | configurations: no | — |
| Configura | `ConfigureFeatureCmd` | — | configurations: no | — |
| Espandi gruppo | `FusionExpandGroupFeatureCommand` | — | yes (available) | — |
| Crea gruppo | `FusionCreateGroupFeatureCommand` | `TimelineGroups.add` | yes (available) | yes |
| BaseFeatureCreation | `BaseFeatureCreation` | `BaseFeatures` | yes (available) | yes |
| TSplineBaseFeatureCreation | `TSplineBaseFeatureCreation` | `FormFeatures` | yes (available) | yes |
| Interrompi collegamento | `BreakWorkingModelLinkCmd` | — | yes (available) | — |
| Rinomina | `FusionRenameTimelineEntryCommand` | `TimelineObject.name` | yes (available) | yes |
| RollToEndCommand | `RollToEndCommand` | `Timeline.moveToEnd` | yes (available) | yes |
| Scorrimento contrassegno timeline qui | `FusionRollCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Converti in lavorazione MD | `ConvertToDMFeatureCommand` | — | yes (available) | — |
| Converti in Parametrica | `ConvertToPMFeatureCommand` | — | yes (available) | — |
| Sopprimi lavorazioni | `FusionSuppressCommand` | `TimelineObject.isSuppressed` | yes (available) | yes |
| Scopri lavorazioni | `FusionUnsuppressCommand` | `TimelineObject.isSuppressed` | yes (available) | yes |
| Attiva configurazione | `DesignConfigurationActivateRowCmd` | — | configurations: no | — |
| Aggiungi configurazione | `DesignConfigurationAddRowCmd` | — | configurations: no | — |
| Elimina configurazione | `DesignConfigurationDeleteRowCmd` | — | configurations: no | — |
| Copia in nuova configurazione | `DesignConfigurationCopyRowCmd` | — | configurations: no | — |
| Esamina avvertimento | `FusionLookupErrInfoCommand` | — | yes (available) | — |
| Rimuovi sostituzioni visibilità | `RemoveVisibilityOverridesCommand` | `RemoveFeatures` | yes (available) | no |
| FusionDesignAdviceFindInTable | `FusionDesignAdviceFindInTable` | — | yes (available) | — |
| Modifica unità attive | `FusionChangeActiveUnitsCommand` | `FusionUnitsManager.distanceDisplayUnits` | yes (available) | yes |
| Modifica tipo di progettazione | `FusionChangeDesignDocTypeCmd` | `Design.designType` | yes (available) | yes |
| Elemento Shell superficie media | `FusionSurfaceMidsurfaceShellCommand` | — | yes (available) | — |
| Shell di offset | `FusionSurfaceOffsetShellCommand` | `OffsetFeatures` | yes (available) | no |
| Shell dalla superficie | `SurfaceShellConvertCommand` | `ShellFeatures` | yes (available) | yes |
| Attiva/disattiva raggio | `ToggleRadialDimCmd` | — | yes (available) | no |
| Attiva/disattiva diametro | `ToggleDiameterDimCmd` | — | yes (available) | no |
| Attiva/disattiva non parametrica | `ToggleDrivenDimCmd` | — | yes (available) | no |
| Attiva/disattiva parametrica | `ToggleDrivingDimCmd` | — | yes (available) | no |
| ToggleMinimumTanDimCmd | `ToggleMinimumTanDimCmd` | — | yes (available) | no |
| ToggleMaximumTanDimCmd | `ToggleMaximumTanDimCmd` | — | yes (available) | no |
| Aggiungi quota offset | `OffsetDimensionCmd` | `OffsetFeatures` | yes (available) | no |
| Modifica offset | `OffsetSketchEdit` | `Sketch` | yes (available) | no |
| Modifica elemento Shell superficie media | `FusionSurfaceMidsurfaceShellEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica elemento Shell superficie | `FusionSurfaceShellEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| MeshDeleteTrianglesCommand | `MeshDeleteTrianglesCommand` | — | yes (available) | — |
| Vincoli | `SketchGeomConstraintCmd` | `GeometricConstraints` | yes (available) | yes |
| Project | `Project` | `Sketch.project` | yes (available) | yes |
| Sposta | `FusionMoveComponentsCommand` | `MoveFeatures` | yes (available) | yes |
| FusionCreateEmptyComponentCommand | `FusionCreateEmptyComponentCommand` | `Occurrences.addNewComponent` | yes (available) | yes |
| FusionCreateComponentFromBodyCommand | `FusionCreateComponentFromBodyCommand` | `BRepBody.createComponent` | yes (available) | yes |
| Ombreggiatura piatta | `ParaMeshFlatMeshShadingCommand` | — | yes (available) | — |
| Ombreggiatura uniforme | `ParaMeshSmoothMeshShadingCommand` | — | yes (available) | — |
| Modifica lavorazione  | `ParaMeshBaseFeatureActivateCommand` | — | yes (available) | — |
| Modifica lavorazione | `ParaMeshDcSmoothEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcSmoothBoundaryEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcHollowEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcReduceEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcCombineEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcRepairEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcToQuadMeshEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcRemeshEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcPlaneCutEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcTessellateEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcConvertEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcExtractEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcCalculateFaceGroupsEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcMoveCopyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcReverseNormalsEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcScaleEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcBridgeEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcMergeFaceGroupsEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcPlanarSectionEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica lavorazione | `ParaMeshDcTextureEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Rimuovi | `VolFieldRemoveModelCommand` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Converti modello volumetrico in mesh | `VolFieldModelToMeshCommand` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Opzioni di visualizzazione volumetrica | `VolFieldDisplayOptionsCommand` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| VolFieldDcCreateModelEditCmd | `VolFieldDcCreateModelEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcSolidityOffsetEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcSolidityAlongPathEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcAddLatticeEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcVolumetricModelEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcCreateLatticeEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcModelToMeshEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |
| Modifica lavorazione | `VolFieldDcTextureEditCmd` | `VolumetricModelFeatures 🧪` | yes (available) | no |

## Manufacture (CNC) / Fresatura tab (`MillingTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Nuovo Setup | `CreateSetupCmd` | `Setups` | yes (available) | yes |
| Crea programma NC | `IronNcProgram` | `NCPrograms` | yes (available) | no |
| Nuova cartella | `IronFolder` | `CAMFolders` | yes (available) | no |
| Nuova serie | `IronPattern` | `CAMPatterns` | yes (available) | no |
| NC manuale | `IronStrategy_manual` | `operations.createInput("manual")` | yes (available) | yes |
| Ispezione per WCS | `IronStrategy_probe` | `operations.createInput("probe")` | probing/inspection: no | yes |
| Nuovo gruppo setup | `CreateSetupGroupCmd` | `Setups` | yes (available) | yes |
| Orientamento utensile | `IronStrategy_tool_orientation` | `operations.createInput("tool_orientation")` | CAM 3+2 / multi-axis: no | yes |
| Inserisci dati di produzione | `IronImportAllCAMXRefsCmd` | — | yes (available) | — |
| Debug parametri oggetti CAD | `IronStrategy_debug_cad_objects` | `operations.createInput("debug_cad_objects")` | yes (available) | yes |
| Crea modello di produzione | `MSFWmdCreateAggregationAssetWorkingModelCmd` | `ManufacturingModels` | yes (available) | no |
| Riconoscimento lavorazione | `IronStrategy_featureRecognition` | `operations.createInput("featureRecognition")` | yes (available) | yes |
| Sgrossatura adattiva 2D | `IronStrategy_adaptive2d` | `operations.createInput("adaptive2d")` | yes (available) | yes |
| Sgrossatura offset 2D (tasca) | `IronStrategy_pocket2d` | `operations.createInput("pocket2d")` | yes (available) | yes |
| Spianatura | `IronStrategy_face` | `operations.createInput("face")` | yes (available) | yes |
| Contornatura 2D | `IronStrategy_contour2d` | `operations.createInput("contour2d")` | yes (available) | yes |
| Asola | `IronStrategy_slot` | `operations.createInput("slot")` | yes (available) | yes |
| Traccia | `IronStrategy_path3d` | `operations.createInput("path3d")` | yes (available) | yes |
| Filettatura | `IronStrategy_thread` | `operations.createInput("thread")` | yes (available) | yes |
| Fresatura elicoidale | `IronStrategy_bore` | `operations.createInput("bore")` | yes (available) | yes |
| Circolare | `IronStrategy_circular` | `operations.createInput("circular")` | yes (available) | yes |
| Incisione | `IronStrategy_engrave` | `operations.createInput("engrave")` | yes (available) | yes |
| Smussatura | `IronStrategy_chamfer2d` | `operations.createInput("chamfer2d")` | yes (available) | yes |
| Sgrossatura adattiva 3D | `IronStrategy_adaptive` | `operations.createInput("adaptive")` | yes (available) | yes |
| Sgrossatura offset 3D (tasca) | `IronStrategy_pocket_new` | `operations.createInput("pocket_new")` | yes (available) | yes |
| Sgrossatura 3+2 | `IronStrategy_moduleworks_three_plus_two` | `operations.createInput("moduleworks_three_plus_two")` | CAM 3+2 / multi-axis: no | yes |
| Distanza di sicurezza area modello | `IronStrategy_model_area_clearance` | `operations.createInput("model_area_clearance")` | yes (available) | yes |
| Ripido e bassa pendenza | `IronStrategy_steep_and_shallow` | `operations.createInput("steep_and_shallow")` | yes (available) | yes |
| Piana | `IronStrategy_flat` | `operations.createInput("flat")` | yes (available) | yes |
| Parete | `IronStrategy_inclined_walls` | `operations.createInput("inclined_walls")` | yes (available) | yes |
| Parallelo | `IronStrategy_parallel_new` | `operations.createInput("parallel_new")` | yes (available) | yes |
| Scallop | `IronStrategy_scallop_new` | `operations.createInput("scallop_new")` | yes (available) | yes |
| Contornatura 3D | `IronStrategy_contour_new` | `operations.createInput("contour_new")` | yes (available) | yes |
| Rampa | `IronStrategy_ramp` | `operations.createInput("ramp")` | yes (available) | yes |
| Bitangenza | `IronStrategy_pencil_new` | `operations.createInput("pencil_new")` | yes (available) | yes |
| Orizzontale | `IronStrategy_horizontal_new` | `operations.createInput("horizontal_new")` | yes (available) | yes |
| Spirale | `IronStrategy_spiral_new` | `operations.createInput("spiral_new")` | yes (available) | yes |
| Radiale | `IronStrategy_radial_new` | `operations.createInput("radial_new")` | yes (available) | yes |
| Spirale con morphing | `IronStrategy_morphed_spiral` | `operations.createInput("morphed_spiral")` | yes (available) | yes |
| Proiezione | `IronStrategy_project` | `operations.createInput("project")` | yes (available) | yes |
| Blend | `IronStrategy_blend` | `operations.createInput("blend")` | yes (available) | yes |
| Morphing | `IronStrategy_morph` | `operations.createInput("morph")` | yes (available) | yes |
| Angolo | `IronStrategy_rest_finishing` | `operations.createInput("rest_finishing")` | yes (available) | yes |
| Flusso (obsoleto) | `IronStrategy_flow` | `operations.createInput("flow")` | yes (available) | yes |
| Flow | `IronStrategy_flow2` | `operations.createInput("flow2")` | yes (available) | yes |
| Smusso 3D | `IronStrategy_chamfer` | `operations.createInput("chamfer")` | yes (available) | yes |
| Sbavatura | `IronStrategy_moduleworks_automatic_deburring` | `operations.createInput("moduleworks_automatic_deburring")` | yes (available) | yes |
| Geodetica | `IronStrategy_moduleworks_geodesic` | `operations.createInput("moduleworks_geodesic")` | yes (available) | yes |
| Punta | `IronStrategy_drill` | `operations.createInput("drill")` | yes (available) | yes |
| Riconoscimento fori | `IronHoleRecognition` | `CAMHoleRecognition` | yes (available) | no |
| Gestione fori | `IronHoleManager` | `CAMHoleRecognition` | yes (available) | no |
| Lavorazione fori | `IronMachineHoles` | `CAMHoleRecognition` | yes (available) | no |
| Sgrossatura offset rotativa (tasca) | `IronStrategy_moduleworks_4axis_roughing` | `operations.createInput("moduleworks_4axis_roughing")` | yes (available) | yes |
| Sgrossatura multi-asse | `IronStrategy_moduleworks_multiaxis_roughing` | `operations.createInput("moduleworks_multiaxis_roughing")` | CAM 3+2 / multi-axis: no | yes |
| Swarf | `IronStrategy_swarf5d` | `operations.createInput("swarf5d")` | CAM 3+2 / multi-axis: no | yes |
| Swarf avanzato | `IronStrategy_moduleworks_swarf` | `operations.createInput("moduleworks_swarf")` | CAM 3+2 / multi-axis: no | yes |
| Contornatura multi-asse | `IronStrategy_multiAxisContour` | `operations.createInput("multiAxisContour")` | CAM 3+2 / multi-axis: no | yes |
| Rotazione parallela | `IronStrategy_rotary_finishing` | `operations.createInput("rotary_finishing")` | CAM 3+2 / multi-axis: no | yes |
| Contornatura rotativa | `IronStrategy_moduleworks_4axis_finishing` | `operations.createInput("moduleworks_4axis_finishing")` | yes (available) | yes |
| Finitura multi-asse | `IronStrategy_moduleworks_multiaxis_finishing` | `operations.createInput("moduleworks_multiaxis_finishing")` | CAM 3+2 / multi-axis: no | yes |
| CAM automatizzato | `IronAutomatedCAM` | `MachiningPlan 🧪` | yes (available) | no |
| Ritaglia | `IronToolpathTrim` | — | yes (available) | — |
| Elimina passate | `IronToolpathEditDelete` | — | yes (available) | — |
| Passi e collegamenti | `IronToolpathEditLeadsLinks` | — | yes (available) | — |
| Sostituisci utensile | `IronToolpathEditToolChange` | — | yes (available) | — |
| Sposta posizioni di ingresso | `IronToolpathEditMoveStartPoints` | — | yes (available) | — |
| Velocità di avanzamento | `IronToolpathEditFeedrate` | — | yes (available) | — |
| Genera | `IronGenerateToolpath` | `CAM.generateToolpath` | yes (available) | yes |
| Simula | `IronSimulation` | — | yes (available) | — |
| Simula con la macchina | `IronMachineSimulation` | — | yes (available) | — |
| Post processa | `IronPostProcess` | `CAM.postProcess` | yes (available) | yes |
| Foglio di lavoro | `IronSetupSheetSwitchboard` | `CAM` | yes (available) | yes |
| Tempo di lavorazione | `IronMachiningTime` | `CAM.getMachiningTime` | yes (available) | yes |
| Fresa di forma | `IronStrategy_create_form_mill` | `operations.createInput("create_form_mill")` | yes (available) | yes |
| Pinza utensile di tornitura | `IronTurningToolHolder` | `TurningTool.holderGeometry` | yes (available) | no |
| Portautensile | `IronToolBlock` | `ToolBlock` | yes (available) | no |
| Pinza utensile di fresatura | `IronStrategy_SolidHolderMilling` | `operations.createInput("SolidHolderMilling")` | yes (available) | yes |
| Librerie utensili | `IronToolLibrary` | `DocumentToolLibrary` | yes (available) | yes |
| Libreria materiali grezzi | `IronStockMaterialLibrary` | `DocumentStockMaterialLibrary` | yes (available) | no |
| Libreria macchine | `IronMachineLibrary` | `MachineLibrary` | yes (available) | no |
| Libreria post | `IronPostLibrary` | `PostLibrary` | yes (available) | yes |
| Libreria Template | `IronTemplateLibrary` | `CAMTemplateLibrary` | yes (available) | no |
| Configurazione fogli di lavoro | `IronSetupSheetConfigurations` | `CAM.generateSetupSheet` | yes (available) | no |
| Gestione attività | `IronTaskManager` | — | yes (available) | — |
| Esporta valori di default | `IronExportDefaults` | — | yes (available) | — |
| Importa valori di default | `IronImportDefaults` | — | yes (available) | — |
| Ripristina valori di default | `IronResetDefaults` | — | yes (available) | — |
| Barra di selezione | `AdvancedDirectSelectionIronParam` | `Selections` | yes (available) | no |

## Manufacture (CNC) / Tornitura tab (`TurningTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Tornitura - Faccia | `IronStrategy_turningFace` | `operations.createInput("turningFace")` | yes (available) | yes |
| Tornitura - Sgrossatura profilo | `IronStrategy_turningProfileRoughing` | `operations.createInput("turningProfileRoughing")` | yes (available) | yes |
| Tornitura - Finitura profilo | `IronStrategy_turningProfileFinishing` | `operations.createInput("turningProfileFinishing")` | yes (available) | yes |
| Tornitura - Sgrossatura gola | `IronStrategy_turningGrooveRoughing` | `operations.createInput("turningGrooveRoughing")` | yes (available) | yes |
| Finitura tornitura gola | `IronStrategy_turningGrooveFinishing` | `operations.createInput("turningGrooveFinishing")` | yes (available) | yes |
| Tornitura - Profilatura | `IronStrategy_turningRoughing` | `operations.createInput("turningRoughing")` | yes (available) | yes |
| Tornitura - Sgrossatura adattiva | `IronStrategy_turningAdaptiveRoughing` | `operations.createInput("turningAdaptiveRoughing")` | yes (available) | yes |
| Tornitura - Gola | `IronStrategy_turningProfileGroove` | `operations.createInput("turningProfileGroove")` | yes (available) | yes |
| Tornitura - Gola singola | `IronStrategy_turningGroove` | `operations.createInput("turningGroove")` | yes (available) | yes |
| Tornitura - Filetto | `IronStrategy_turningThread` | `operations.createInput("turningThread")` | yes (available) | yes |
| Tornitura - Smusso | `IronStrategy_turningChamfer` | `operations.createInput("turningChamfer")` | yes (available) | yes |
| Tornitura - Taglio | `IronStrategy_turningPart` | `operations.createInput("turningPart")` | yes (available) | yes |
| Tornitura - Traccia | `IronStrategy_turningTrace` | `operations.createInput("turningTrace")` | yes (available) | yes |
| Presa contromandrino | `IronStrategy_turningSecondarySpindleGrab` | `operations.createInput("turningSecondarySpindleGrab")` | yes (available) | yes |
| Estrazione barra | `IronStrategy_turningSecondarySpindlePull` | `operations.createInput("turningSecondarySpindlePull")` | yes (available) | yes |
| Ritorno contromandrino | `IronStrategy_turningSecondarySpindleReturn` | `operations.createInput("turningSecondarySpindleReturn")` | yes (available) | yes |
| Chiamata utensile | `IronStrategy_turningToolCall` | `operations.createInput("turningToolCall")` | yes (available) | yes |

## Manufacture (CNC) / Additivo tab (`AdditiveTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Nuovo setup da G-Code | `IronAdditiveImportGCode` | — | yes (available) | — |
| Sposta componenti | `CAMMoveComponentsCommand` | — | yes (available) | — |
| Altezza minima costruzione | `IronMinimizeBoundingBox` | — | yes (available) | — |
| Orientamento automatico | `IronStrategy_additive_optimize_orientation` | `operations.createInput("additive_optimize_orientation")` | yes (available) | yes |
| Disponi | `IronStrategy_additive_arrange_strategy` | `operations.createInput("additive_arrange_strategy")` | yes (available) | yes |
| Gruppo di subnest | `IronStrategy_additive_subnest_strategy` | `operations.createInput("additive_subnest_strategy")` | nesting: paid extension — to be verified | yes |
| Posiziona su piattaforma | `IronPlaceOnPlatform` | — | yes (available) | — |
| Analisi interferenze | `IronStrategy_additive_interference_analysis` | `operations.createInput("additive_interference_analysis")` | yes (available) | yes |
| Volume di costruzione di riempimento | `FillPlatformCmd` | — | yes (available) | — |
| Duplica | `LinearArrangeCmd` | — | yes (available) | — |
| Assegna preset corpo | `IronAssignBuildStrategy` | `AdditiveSetupUtility.assignPartsToBodyPreset` | yes (available) | no |
| Dividi supporti | `SplitSupportCmd` | `AdditiveSetupUtility.splitSupport` | yes (available) | no |
| Rimuovi componenti | `RemoveExcessParts` | `AdditiveSetupUtility.removeExcessParts` | yes (available) | no |
| Supporto volumetrico | `IronStrategy_areavolume_additive_support` | `operations.createInput("areavolume_additive_support")` | yes (available) | yes |
| Supporto volumetrico | `IronStrategy_areavolume_additive_fff_support` | `operations.createInput("areavolume_additive_fff_support")` | yes (available) | yes |
| Volume circostante per supporto polilinea | `IronStrategy_surroundvolumepolyline_additive_support` | `operations.createInput("surroundvolumepolyline_additive_support")` | yes (available) | yes |
| Supporto della barra | `IronStrategy_areabar_additive_support` | `operations.createInput("areabar_additive_support")` | yes (available) | yes |
| Supporto barra solido | `IronStrategy_areabar_additive_fff_support` | `operations.createInput("areabar_additive_fff_support")` | yes (available) | yes |
| Supporto barra dei punti rivolta verso il basso | `IronStrategy_downoriented_additive_support` | `operations.createInput("downoriented_additive_support")` | yes (available) | yes |
| Supporto reticolo | `IronStrategy_lattice_additive_support` | `operations.createInput("lattice_additive_support")` | yes (available) | yes |
| Spigolo con supporto barra | `IronStrategy_edgebar_additive_support` | `operations.createInput("edgebar_additive_support")` | yes (available) | yes |
| Supporto polilinea | `IronStrategy_areapolyline_additive_support` | `operations.createInput("areapolyline_additive_support")` | yes (available) | yes |
| Spigolo con supporto polilinea | `IronStrategy_edgepolyline_additive_support` | `operations.createInput("edgepolyline_additive_support")` | yes (available) | yes |
| Contornatura cluster con supporto polilinea | `IronStrategy_clustercontourpolyline_additive_support` | `operations.createInput("clustercontourpolyline_additive_support")` | yes (available) | yes |
| Asse mediano con supporto polilinea | `IronStrategy_skeletonpolyline_additive_support` | `operations.createInput("skeletonpolyline_additive_support")` | yes (available) | yes |
| Supporto piastra base | `IronStrategy_baseplate_additive_support` | `operations.createInput("baseplate_additive_support")` | yes (available) | yes |
| Supporto per il setter | `IronStrategy_setter_additive_support` | `operations.createInput("setter_additive_support")` | yes (available) | yes |
| Supporto laterale | `IronStrategy_lateral_additive_support` | `operations.createInput("lateral_additive_support")` | yes (available) | yes |
| Elimina supporti | `IronStrategy_delete_additive_supports` | `operations.createInput("delete_additive_supports")` | yes (available) | yes |
| Costruzione lavorazione | `IronStrategy_feature_construction` | `operations.createInput("feature_construction")` | yes (available) | yes |
| Studio | `IronStrategy_AdditiveProcessSimulation` | `operations.createInput("AdditiveProcessSimulation")` | additive process simulation: paid extension — to be verified | yes |
| PreCheck | `IronAdditiveProcessSimPreCheck` | — | additive process simulation: paid extension — to be verified | — |
| Risolvi | `IronAdditiveProcessSimSolve` | — | additive process simulation: paid extension — to be verified | — |
| Visualizza mesh | `IronAdditiveMeshView` | — | additive process simulation: paid extension — to be verified | — |
| Visualizza risultati | `IronAdditiveResultsView` | — | additive process simulation: paid extension — to be verified | — |
| Simula percorso utensile additivo | `IronAdditiveSimulation` | — | yes (available) | — |
| Crea file di costruzione macchina | `IronStrategy_additive_exportstrategy` | `operations.createInput("additive_exportstrategy")` | yes (available) | yes |
| Crea file di costruzione macchina | `IronStrategy_additive_formlabs_exportstrategy` | `operations.createInput("additive_formlabs_exportstrategy")` | yes (available) | yes |
| Stampa statistiche | `IronAdditiveShowPrintStatistics` | — | yes (available) | — |
| Statistiche piattaforma | `IronAdditiveShow3DPackingDensity` | — | yes (available) | — |
| Analisi delle sezioni | `IronAdditiveSliceStatistics` | — | yes (available) | — |
| Esportazione scena 3MF | `IronStrategy_additive_3mf_exportstrategy` | `operations.createInput("additive_3mf_exportstrategy")` | yes (available) | yes |
| Libreria impostazioni di stampa | `IronPrintSettingLibrary` | `PrintSettingLibrary` | yes (available) | no |

## Manufacture (CNC) / Risultati tab (`AdditiveResultsTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Attiva/disattiva spigoli elemento | `IronAdditiveProcessSimToggleEdges` | — | additive process simulation: paid extension — to be verified | — |
| Attiva/disattiva punti di indagine min/max | `IronAdditiveProcessSimMinMaxProbe` | — | additive process simulation: paid extension — to be verified | — |
| Apri cartella risultati | `IronAdditiveOpenResultsFolder` | — | additive process simulation: paid extension — to be verified | — |
| Esportazione compensata | `IronAdditiveExportCompensated` | — | additive process simulation: paid extension — to be verified | — |
| Esporta STL compensato | `IronAdditiveExportCompensatedSTL` | — | additive process simulation: paid extension — to be verified | — |
| Esporta STL deformato | `IronAdditiveExportWarpedSTL` | — | additive process simulation: paid extension — to be verified | — |
| Esporta 3MF a colori | `IronAdditiveExportColor3MF` | `CAM3MFExportOptions` | yes (available) | no |
| Termina risultati | `AdditiveResultsStop` | — | yes (available) | — |

## Manufacture (CNC) / Ispezione tab (`ProbingTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Geometria ispezione | `IronStrategy_probe_geometry` | `operations.createInput("probe_geometry")` | probing/inspection: no | yes |
| Ispezione superficie | `IronStrategy_inspectSurface` | `operations.createInput("inspectSurface")` | probing/inspection: no | yes |
| Crea piano di ispezione | `IronCreateInspectionPlan` | — | yes (available) | — |
| Allineamento parte | `PartAlignmentStart_Delayed` | — | probing/inspection: no | — |
| Allineamento parte in tempo reale | `PartAlignmentStart_Live` | — | probing/inspection: no | — |
| Setup ispezione CMM | `IronStrategy_cmm_inspection_setup` | `operations.createInput("cmm_inspection_setup")` | yes (available) | yes |
| Allinea CAD alla parte | `IronStrategy_datum` | `operations.createInput("datum")` | yes (available) | yes |
| Ispeziona manualmente superficie | `MeasureSurface` | — | yes (available) | — |
| Scansione superficie | `ScanSurface` | — | yes (available) | — |
| Crea ispezione manuale | `IronCreateInspections` | — | yes (available) | — |
| Registra ispezione manuale | `IronRecordManualMeasure` | — | yes (available) | — |
| Importa risultati di ispezione | `ImportResults` | — | yes (available) | — |
| Connessione in tempo reale | `LiveProbing` | — | probing/inspection: no | — |
| Rapporto di ispezione | `IronInspectionReport` | — | yes (available) | — |

## Manufacture (CNC) / Fabbricazione tab (`FabricationTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Origini componenti | `MSFWmdComponentLibraryCmd` | — | yes (available) | — |
| Crea studio nest | `MSFNestPrepareNestCmd` | — | nesting: paid extension — to be verified | — |
| Genera | `MSF.MAGNestCalculateCmd.Generate` | — | nesting: paid extension — to be verified | — |
| Profilo 2D | `IronStrategy_jet2d` | `operations.createInput("jet2d")` | yes (available) | yes |
| Libreria dei materiali del processo | `MSF.MAGMatLibraryCmd.FusionNesting` | — | nesting: paid extension — to be verified | — |
| Preset per materiale e formato | `MSF.MSFNestSaveContainerDataCmd.Create` | — | nesting: paid extension — to be verified | — |
| Denominazione automatica | `MSFNestNameConventionCmd` | — | nesting: paid extension — to be verified | — |

## Manufacture (CNC) / Utilità tab (`UtilitiesTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Generazione automatica materiale grezzo in lavorazione | `IronAutomaticIPSGeneration` | — | yes (available) | — |
| Cancella cache materiale grezzo in lavorazione | `IronClearIPSCache` | — | yes (available) | — |
| Genera IPS GPU in base al setup | `IronGPU_IPSTest` | — | yes (available) | — |

## Manufacture (CNC) / Allineamento parte tab (`PartAlignmentTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Modifica allineamento | `PartAlignment_EditAlignment` | — | probing/inspection: no | — |
| Ispezione superficie | `PartAlignment_IronStrategy_inspectSurface` | — | probing/inspection: no | — |
| Post per allineamento | `PartAlignment_IronNcProgram` | — | probing/inspection: no | — |
| Importa risultati di ispezione | `PartAlignment_ImportResults` | — | probing/inspection: no | — |
| Mostra informazioni di allineamento parte | `PartAlignment_IronPartAlignmentInfo` | — | probing/inspection: no | — |
| Mostra risultati | `PartAlignment_IronShowResults` | — | probing/inspection: no | — |
| Post con allineamento | `PartAlignmentPostStop` | — | probing/inspection: no | — |
| Allineamento parte di uscita | `PartAlignmentStop_Delayed` | — | probing/inspection: no | — |

## Manufacture (CNC) / Allineamento parte in tempo reale tab (`LiveAlignmentTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Post per allineamento in tempo reale | `PartAlignmentPostLive` | — | probing/inspection: no | — |
| Connessione in tempo reale | `LivePartAlignment` | — | probing/inspection: no | — |
| Esci da Allineamento parte in tempo reale | `PartAlignmentStop_Live` | — | probing/inspection: no | — |

## Manufacture (CNC) / Simulazione tab (`SimulationTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Pinza | `SimulationShowToolHolder` | — | yes (available) | — |
| Gambo | `SimulationShowToolShaft` | — | yes (available) | — |
| Tagliente | `SimulationShowToolFlute` | — | yes (available) | — |
| Nascondi utensile | `SimulationHideTool` | — | yes (available) | — |
| Macchina | `SimulationShowHideMachine` | — | yes (available) | — |
| Percorsi utensile | `SimulationShowHideToolpath` | — | yes (available) | — |
| Materiale grezzo | `SimulationShowHideStock` | — | yes (available) | — |
| Problemi | `SimulationIssues` | — | yes (available) | — |
| Codice NC | `SimulationNCCode` | — | yes (available) | — |
| Materiale grezzo da modellare | `SimulationStockToModel` | — | yes (available) | — |
| Simula più rapidamente (GPU) | `ToggleSimulationEngine` | — | yes (available) | — |
| Esci dalla simulazione | `SimulationStop` | — | yes (available) | — |

## Manufacture (CNC) / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| FusionDcEditWorkPlaneAlongPathCommand | `FusionDcEditWorkPlaneAlongPathCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisThroughCylinderCommand | `FusionDcEditWorkAxisThroughCylinderCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisFromLineCommand | `FusionDcEditWorkAxisFromLineCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisFromTwoPointsCommand | `FusionDcEditWorkAxisFromTwoPointsCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisFromTwoPlanesCommand | `FusionDcEditWorkAxisFromTwoPlanesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisNormalToFaceCommand | `FusionDcEditWorkAxisNormalToFaceCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Importa | `NeuCAMImportCommand` | `ImportManager` | yes (available) | yes |
| Modifica | `IronEditOperation` | `Operation.parameters` | yes (available) | yes |
| Modifica ispezioni manuali | `IronEditInspections` | — | yes (available) | — |
| Modifica modello di produzione per Setup | `IronEditWorkingModelSetup` | — | yes (available) | — |
| Modifica | `IronAdditiveEditPrintSetting` | `Documents.add` | yes (available) | yes |
| Modifica | `IronEditHoleRecognition` | — | yes (available) | — |
| Modifica | `IronEditMachineHoles` | — | yes (available) | — |
| Modifica | `IronEditNcProgram` | `NCProgram` | yes (available) | no |
| Modifica utensile | `IronEditTool` | `Tool` | yes (available) | yes |
| Modifica segno foro | `IronEditHoleSignature` | — | yes (available) | — |
| Confronta e modifica | `IronCompareAndEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| IronCompareAndEditRework | `IronCompareAndEditRework` | — | yes (available) | — |
| Nuovo supporto | `IronAdditiveSupport` | — | yes (available) | — |
| Nuovo studio | `IronAdditiveOrientations` | — | yes (available) | — |
| Modifica | `IronEditAdditiveProcessSimulation` | — | additive process simulation: paid extension — to be verified | — |
| Genera mesh | `IronAdditiveProcessSimMesh` | — | additive process simulation: paid extension — to be verified | — |
| Cancella risultati della risoluzione | `IronAdditiveDeleteProcSimResults` | — | yes (available) | — |
| Nuova operazione | `IronNewOperation` | `Documents.add` | yes (available) | yes |
| Foratura | `IronDrilling` | — | yes (available) | — |
| Fresatura 2D | `Iron2DMilling` | — | yes (available) | — |
| Fresatura 3D | `Iron3DMilling` | — | yes (available) | — |
| Fresatura multi-asse | `IronMultiAxisMilling` | — | CAM 3+2 / multi-axis: no | — |
| Tornitura | `IronTurning` | — | yes (available) | — |
| Gestione parte | `IronPartHandling` | — | yes (available) | — |
| Trasferimento di materiale grezzo tornitura | `IronStrategy_turningStockTransfer` | `operations.createInput("turningStockTransfer")` | yes (available) | yes |
| Taglio | `IronWLPC` | — | yes (available) | — |
| Ispezione | `IronInspection` | — | yes (available) | — |
| IronStrategy_inspectSurfaceGeometry | `IronStrategy_inspectSurfaceGeometry` | `operations.createInput("inspectSurfaceGeometry")` | probing/inspection: no | yes |
| Crea da modello | `IronCreateFromTemplate` | `Setup.createFromCAMTemplate` | yes (available) | no |
| Gruppo | `IronGroupEditObjects` | `CAMFolders` | yes (available) | no |
| Separa | `IronUngroupEditObjects` | — | yes (available) | — |
| Mostra informazioni di allineamento parte | `IronPartAlignmentInfo` | — | probing/inspection: no | — |
| Ripristino allineamento parte | `IronResetPartAlignment` | — | probing/inspection: no | — |
| Misura allineamento | `MeasureDatum` | — | yes (available) | — |
| Iron3MFExport | `Iron3MFExport` | `Documents.add` | yes (available) | yes |
| Apri cartella di output NC | `IronOpenNcFolder` | `Documents.add` | yes (available) | yes |
| Cancella percorso utensile | `IronClearToolpath` | `CAM.clearToolpath` | yes (available) | no |
| Mostra | `IronDrawAllToolpathOps` | — | yes (available) | — |
| Nascondi | `IronUndrawAllToolpathOps` | — | yes (available) | — |
| Mostra tutto | `IronDrawAllToolpathsInParent` | — | yes (available) | — |
| Nascondi tutto | `IronUndrawAllToolpathsInParent` | — | yes (available) | — |
| Mostra/Nascondi percorso utensile | `IronToolpathVisibilityToggle` | — | yes (available) | no |
| Salva parametri come default | `IronMakeAllDefault` | — | yes (available) | — |
| Sopprimi | `IronSuppress` | `OperationBase.isSuppressed` | yes (available) | yes |
| Proteggi | `IronProtect` | `OperationBase.isProtected` | yes (available) | no |
| Opzionale | `IronOptional` | `OperationBase.isOptional` | yes (available) | no |
| Modifica note | `IronEditNotes` | `OperationBase.notes` | yes (available) | no |
| Crea operazione derivata | `IronDerivedOperation` | `DeriveFeatures` | yes (available) | yes |
| Foratura | `IronDrilling_derived` | — | yes (available) | — |
| Punta | `IronStrategy_drill_derived` | `operations.createInput("drill_derived")` | yes (available) | yes |
| Fresatura 2D | `Iron2DMilling_derived` | — | yes (available) | — |
| Spianatura | `IronStrategy_face_derived` | `operations.createInput("face_derived")` | yes (available) | yes |
| Sgrossatura adattiva 2D | `IronStrategy_adaptive2d_derived` | `operations.createInput("adaptive2d_derived")` | yes (available) | yes |
| Sgrossatura offset 2D (tasca) | `IronStrategy_pocket2d_derived` | `operations.createInput("pocket2d_derived")` | yes (available) | yes |
| Contornatura 2D | `IronStrategy_contour2d_derived` | `operations.createInput("contour2d_derived")` | yes (available) | yes |
| Asola | `IronStrategy_slot_derived` | `operations.createInput("slot_derived")` | yes (available) | yes |
| Circolare | `IronStrategy_circular_derived` | `operations.createInput("circular_derived")` | yes (available) | yes |
| Fresatura elicoidale | `IronStrategy_bore_derived` | `operations.createInput("bore_derived")` | yes (available) | yes |
| Filettatura | `IronStrategy_thread_derived` | `operations.createInput("thread_derived")` | yes (available) | yes |
| Traccia | `IronStrategy_path3d_derived` | `operations.createInput("path3d_derived")` | yes (available) | yes |
| Incisione | `IronStrategy_engrave_derived` | `operations.createInput("engrave_derived")` | yes (available) | yes |
| Smussatura | `IronStrategy_chamfer2d_derived` | `operations.createInput("chamfer2d_derived")` | yes (available) | yes |
| Fresatura 3D | `Iron3DMilling_derived` | — | yes (available) | — |
| Sgrossatura adattiva 3D | `IronStrategy_adaptive_derived` | `operations.createInput("adaptive_derived")` | yes (available) | yes |
| Sgrossatura offset 3D (tasca) | `IronStrategy_pocket_new_derived` | `operations.createInput("pocket_new_derived")` | yes (available) | yes |
| Sgrossatura 3+2 | `IronStrategy_moduleworks_three_plus_two_derived` | `operations.createInput("moduleworks_three_plus_two_derived")` | CAM 3+2 / multi-axis: no | yes |
| Distanza di sicurezza area modello | `IronStrategy_model_area_clearance_derived` | `operations.createInput("model_area_clearance_derived")` | yes (available) | yes |
| Parallelo | `IronStrategy_parallel_new_derived` | `operations.createInput("parallel_new_derived")` | yes (available) | yes |
| Contornatura 3D | `IronStrategy_contour_new_derived` | `operations.createInput("contour_new_derived")` | yes (available) | yes |
| Rampa | `IronStrategy_ramp_derived` | `operations.createInput("ramp_derived")` | yes (available) | yes |
| Orizzontale | `IronStrategy_horizontal_new_derived` | `operations.createInput("horizontal_new_derived")` | yes (available) | yes |
| Bitangenza | `IronStrategy_pencil_new_derived` | `operations.createInput("pencil_new_derived")` | yes (available) | yes |
| Scallop | `IronStrategy_scallop_new_derived` | `operations.createInput("scallop_new_derived")` | yes (available) | yes |
| Spirale | `IronStrategy_spiral_new_derived` | `operations.createInput("spiral_new_derived")` | yes (available) | yes |
| Radiale | `IronStrategy_radial_new_derived` | `operations.createInput("radial_new_derived")` | yes (available) | yes |
| Spirale con morphing | `IronStrategy_morphed_spiral_derived` | `operations.createInput("morphed_spiral_derived")` | yes (available) | yes |
| Proiezione | `IronStrategy_project_derived` | `operations.createInput("project_derived")` | yes (available) | yes |
| Blend | `IronStrategy_blend_derived` | `operations.createInput("blend_derived")` | yes (available) | yes |
| Morphing | `IronStrategy_morph_derived` | `operations.createInput("morph_derived")` | yes (available) | yes |
| Flusso (obsoleto) | `IronStrategy_flow_derived` | `operations.createInput("flow_derived")` | yes (available) | yes |
| Flow | `IronStrategy_flow2_derived` | `operations.createInput("flow2_derived")` | yes (available) | yes |
| Ripido e bassa pendenza | `IronStrategy_steep_and_shallow_derived` | `operations.createInput("steep_and_shallow_derived")` | yes (available) | yes |
| Piana | `IronStrategy_flat_derived` | `operations.createInput("flat_derived")` | yes (available) | yes |
| Parete | `IronStrategy_inclined_walls_derived` | `operations.createInput("inclined_walls_derived")` | yes (available) | yes |
| Angolo | `IronStrategy_rest_finishing_derived` | `operations.createInput("rest_finishing_derived")` | yes (available) | yes |
| Sbavatura | `IronStrategy_moduleworks_automatic_deburring_derived` | `operations.createInput("moduleworks_automatic_deburring_derived")` | yes (available) | yes |
| Geodetica | `IronStrategy_moduleworks_geodesic_derived` | `operations.createInput("moduleworks_geodesic_derived")` | yes (available) | yes |
| Fresatura multi-asse | `IronMultiAxisMilling_derived` | — | CAM 3+2 / multi-axis: no | — |
| Sgrossatura offset rotativa (tasca) | `IronStrategy_moduleworks_4axis_roughing_derived` | `operations.createInput("moduleworks_4axis_roughing_derived")` | yes (available) | yes |
| Sgrossatura multi-asse | `IronStrategy_moduleworks_multiaxis_roughing_derived` | `operations.createInput("moduleworks_multiaxis_roughing_derived")` | CAM 3+2 / multi-axis: no | yes |
| Swarf | `IronStrategy_swarf5d_derived` | `operations.createInput("swarf5d_derived")` | CAM 3+2 / multi-axis: no | yes |
| Swarf avanzato | `IronStrategy_moduleworks_swarf_derived` | `operations.createInput("moduleworks_swarf_derived")` | CAM 3+2 / multi-axis: no | yes |
| Contornatura multi-asse | `IronStrategy_multiAxisContour_derived` | `operations.createInput("multiAxisContour_derived")` | CAM 3+2 / multi-axis: no | yes |
| Rotazione parallela | `IronStrategy_rotary_finishing_derived` | `operations.createInput("rotary_finishing_derived")` | CAM 3+2 / multi-axis: no | yes |
| Contornatura rotativa | `IronStrategy_moduleworks_4axis_finishing_derived` | `operations.createInput("moduleworks_4axis_finishing_derived")` | yes (available) | yes |
| Finitura multi-asse | `IronStrategy_moduleworks_multiaxis_finishing_derived` | `operations.createInput("moduleworks_multiaxis_finishing_derived")` | CAM 3+2 / multi-axis: no | yes |
| Tornitura | `IronTurning_derived` | — | yes (available) | — |
| Tornitura - Sgrossatura profilo | `IronStrategy_turningProfileRoughing_derived` | `operations.createInput("turningProfileRoughing_derived")` | yes (available) | yes |
| Tornitura - Finitura profilo | `IronStrategy_turningProfileFinishing_derived` | `operations.createInput("turningProfileFinishing_derived")` | yes (available) | yes |
| Tornitura - Sgrossatura gola | `IronStrategy_turningGrooveRoughing_derived` | `operations.createInput("turningGrooveRoughing_derived")` | yes (available) | yes |
| Finitura tornitura gola | `IronStrategy_turningGrooveFinishing_derived` | `operations.createInput("turningGrooveFinishing_derived")` | yes (available) | yes |
| Tornitura - Profilatura | `IronStrategy_turningRoughing_derived` | `operations.createInput("turningRoughing_derived")` | yes (available) | yes |
| Tornitura - Sgrossatura adattiva | `IronStrategy_turningAdaptiveRoughing_derived` | `operations.createInput("turningAdaptiveRoughing_derived")` | yes (available) | yes |
| Tornitura - Gola | `IronStrategy_turningProfileGroove_derived` | `operations.createInput("turningProfileGroove_derived")` | yes (available) | yes |
| Tornitura - Faccia | `IronStrategy_turningFace_derived` | `operations.createInput("turningFace_derived")` | yes (available) | yes |
| Tornitura - Gola singola | `IronStrategy_turningGroove_derived` | `operations.createInput("turningGroove_derived")` | yes (available) | yes |
| Tornitura - Smusso | `IronStrategy_turningChamfer_derived` | `operations.createInput("turningChamfer_derived")` | yes (available) | yes |
| Tornitura - Taglio | `IronStrategy_turningPart_derived` | `operations.createInput("turningPart_derived")` | yes (available) | yes |
| Tornitura - Filetto | `IronStrategy_turningThread_derived` | `operations.createInput("turningThread_derived")` | yes (available) | yes |
| Tornitura - Traccia | `IronStrategy_turningTrace_derived` | `operations.createInput("turningTrace_derived")` | yes (available) | yes |
| Gestione parte | `IronPartHandling_derived` | — | yes (available) | — |
| Trasferimento di materiale grezzo tornitura | `IronStrategy_turningStockTransfer_derived` | `operations.createInput("turningStockTransfer_derived")` | yes (available) | yes |
| Presa contromandrino | `IronStrategy_turningSecondarySpindleGrab_derived` | `operations.createInput("turningSecondarySpindleGrab_derived")` | yes (available) | yes |
| Estrazione barra | `IronStrategy_turningSecondarySpindlePull_derived` | `operations.createInput("turningSecondarySpindlePull_derived")` | yes (available) | yes |
| Ritorno contromandrino | `IronStrategy_turningSecondarySpindleReturn_derived` | `operations.createInput("turningSecondarySpindleReturn_derived")` | yes (available) | yes |
| Chiamata utensile | `IronStrategy_turningToolCall_derived` | `operations.createInput("turningToolCall_derived")` | yes (available) | yes |
| Taglio | `IronWLPC_derived` | — | yes (available) | — |
| Profilo 2D | `IronStrategy_jet2d_derived` | `operations.createInput("jet2d_derived")` | yes (available) | yes |
| Innalza di livello | `IronExtractEditSubToolpath` | — | yes (available) | — |
| Modifica | `IronNewToolpathEdit` | `TimelineObject.rollTo` | yes (available) | yes |
| Sposta qui il contrassegno | `IronMoveInsertMarkerHere` | `MoveFeatures` | yes (available) | yes |
| Aggiungi a nuova cartella | `IronAddToNewFolder` | `Documents.add` | yes (available) | yes |
| Aggiungi a nuovo pattern | `IronAddToNewPattern` | `Documents.add` | yes (available) | yes |
| Duplica | `IronDuplicate` | `OperationBase.duplicate` | yes (available) | no |
| Taglia | `IronCut` | — | yes (available) | — |
| Copia | `IronCopy` | `OperationBase.copyAfter` | yes (available) | no |
| Elimina | `IronDeleteObject` | `OperationBase.deleteMe` | yes (available) | yes |
| Elimina | `IronDeleteNonIronObject` | — | yes (available) | — |
| Elimina | `IronDeleteEditSubToolpath` | — | yes (available) | — |
| Elimina modifiche | `IronDiscardEdits` | — | yes (available) | — |
| Risultati orientamento | `IronAdditiveViewOrientationResults` | `Viewport.camera` | yes (available) | yes |
| Interrompi collegamento | `IronBreakLink` | — | yes (available) | — |
| Associa vista con nome | `IronAssociateNamedView` | `Viewport.camera` | yes (available) | yes |
| Mostra dati percorso utensile | `IronViewToolpath` | `Viewport.camera` | yes (available) | yes |
| Mostra registro log | `IronShowLog` | — | yes (available) | no |
| Mostra risultati | `IronShowResults` | — | yes (available) | no |
| Mostra rapporto | `IronAutomatedCAMShowReport` | — | yes (available) | no |
| Modifica ispezione manuale | `IronReplayManualMeasure` | — | yes (available) | — |
| Ricalcola risultati ispezione | `IronRecalculateInspectionResults` | — | yes (available) | — |
| Salva come modello | `IronStoreAsTemplate` | `CAMTemplate.createFromOperations` | yes (available) | no |
| Salva come foro modello | `IronStoreAsHoleTemplate` | — | yes (available) | — |
| Espandi tutti i subordinati | `IronExpandAllChildren` | — | yes (available) | — |
| Comprimi tutti i subordinati | `IronCollapseAllChildren` | — | yes (available) | — |
| Modifica modello di produzione | `ActivateMfgWorkingModelCmd` | `ManufacturingModels` | yes (available) | no |
| Elimina | `DeleteMfgWorkingModelCmd` | — | yes (available) | — |
| Duplica | `DuplicateMfgWorkingModelCmd` | `ManufacturingModel.duplicate` | yes (available) | no |
| Elimina tutti i modelli di produzione | `DeleteMfgWorkingModelsCmd` | — | yes (available) | — |
| Crea setup dalla disposizione | `IronCreateSetupsFromArrangement` | — | yes (available) | — |
| Crea Setup da Inviluppo | `IronCreateSetupFromEnvelope` | — | yes (available) | — |
| Crea Setup dal modello di produzione | `IronCreateSetupFromWorkingModel` | `Setups` | yes (available) | yes |
| Crea Setup dal modello di produzione | `IronCreateSetupsFromWorkingModel` | `Setups` | yes (available) | yes |
| Statistiche Disposizione - Disposizione 2D | `MSFArrangeReportCmdDef` | — | yes (available) | — |
| Statistiche Disposizione - Disposizione 3D | `Simple3dArrangeReportCmdDef` | — | yes (available) | — |
| Statistiche Disposizione- Inviluppo 2D | `MSFEnvelopeReportCmdDef` | — | yes (available) | — |
| Aggiornamento modelli di produzione | `IronUpdateWorkingModels` | — | yes (available) | — |
| Mostra/nascondi linee di piega | `IronToggleBendLineVisibility` | — | yes (available) | no |
| Modifica macchina... | `MachineBrowserEntry_EditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| Aggiorna modello macchina | `UpdateMachineModelCmd` | — | yes (available) | — |
| Rimuovi macchina | `MachineBrowserEntry_RemoveCmd` | — | yes (available) | — |
| Sostituisci macchina | `MachineBrowserEntry_ReplaceCmd` | `Machine` | yes (available) | no |
| Rimuovi dal setup | `MachineBrowserEntry_RemoveFromSetupCmd` | — | yes (available) | — |
| Opzioni di visualizzazione raccordo geometrico | `IronResultDisplaySettings` | `Viewport.camera` | yes (available) | yes |
| Crea gruppo di selezione | `IronCreateSelectionGroupCmd` | `Selections` | yes (available) | no |
| Mostra/Nascondi | `CAMVisibilityToggleCmdDef` | — | yes (available) | no |
| Mostra tutti i componenti | `CAMShowAllComponentsCmdDef` | — | yes (available) | no |
| Mostra tutti i corpi | `CAMShowAllBodiesCmdDef` | — | yes (available) | no |
| Isola | `IronIsolateCmd` | — | yes (available) | no |
| Rimuovi isolamento | `IronUnisolateCmd` | — | yes (available) | — |
| Rimuovi isolamento per tutti | `IronUnisolateAllCmd` | — | yes (available) | — |
| Inserisci dati di produzione | `IronImportCAMXRefCmd` | `Documents.add` | yes (available) | yes |
| Trova nel browser | `IronFindInBrowser` | — | yes (available) | — |
| Crea elenco di taglio | `MSFNestCutListCmdDef` | — | nesting: paid extension — to be verified | — |
| WorkPlaneOffsetFromPlaneCommand | `WorkPlaneOffsetFromPlaneCommand` | — | yes (available) | — |
| WorkAxisThroughCylinderCommand | `WorkAxisThroughCylinderCommand` | — | yes (available) | — |
| PCBReplaceComponentCmdDef | `PCBReplaceComponentCmdDef` | — | yes (available) | — |
| FusionDcEditWorkPlaneByPlaneOffsetCommand | `FusionDcEditWorkPlaneByPlaneOffsetCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneByLineAndAngleCommand | `FusionDcEditWorkPlaneByLineAndAngleCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneFromTwoPlanesCommand | `FusionDcEditWorkPlaneFromTwoPlanesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneFromTwoLinesCommand | `FusionDcEditWorkPlaneFromTwoLinesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneTangentToCylinderCommand | `FusionDcEditWorkPlaneTangentToCylinderCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneTangentToFaceAtPointCommand | `FusionDcEditWorkPlaneTangentToFaceAtPointCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPlaneFromThreePointsCommand | `FusionDcEditWorkPlaneFromThreePointsCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkAxisFromPointAndFaceCommand | `FusionDcEditWorkAxisFromPointAndFaceCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPointCommand | `FusionDcEditWorkPointCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPointFromTwoLinesCommand | `FusionDcEditWorkPointFromTwoLinesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPointFromThreePlanesCommand | `FusionDcEditWorkPointFromThreePlanesCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPointFromLineAndPlaneCommand | `FusionDcEditWorkPointFromLineAndPlaneCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| FusionDcEditWorkPointFromCircleOrSphereCommand | `FusionDcEditWorkPointFromCircleOrSphereCommand` | `SketchCircles` | yes (available) | yes |
| FusionDcEditWorkPointAlongPathCommand | `FusionDcEditWorkPointAlongPathCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica | `MeshBaseFeatureActivate` | `BaseFeatures` | yes (available) | yes |
| SheetMetalBendEditCmd | `SheetMetalBendEditCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| EditConstraintCmd | `EditConstraintCmd` | — | yes (available) | — |
| DcEditConstraintCmd | `DcEditConstraintCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| EditAutoJointInferenceCmd | `EditAutoJointInferenceCmd` | — | yes (available) | — |
| DcEditAutoJointInferenceCmd | `DcEditAutoJointInferenceCmd` | `TimelineObject.rollTo` | yes (available) | yes |
| SelectJointComponentsCmd | `SelectJointComponentsCmd` | `Selections` | yes (available) | no |
| MeshBaseFeatureCreation | `MeshBaseFeatureCreation` | `BaseFeatures` | yes (available) | yes |
| Termina mesh | `MeshBaseFeatureStop` | `BaseFeatures` | yes (available) | yes |
| Mesh2BRepCommand | `Mesh2BRepCommand` | `MeshConvertFeatures 🧪` | yes (available) | yes |
| BRep2MeshCommand | `BRep2MeshCommand` | — | yes (available) | — |
| InsertAlignMeshCommand | `InsertAlignMeshCommand` | — | yes (available) | — |

## Drawing / DISEGNO tab (`FusionDocTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Vista di base | `FusionDrawingViewBaseCommand` | `BaseViewInput 🧪` | yes (available) | no |
| Segnaposto vista di base | `FusionDrawingViewBaseTemplateCommand` | `BaseViewInput 🧪` | yes (available) | no |
| Vista proiettata | `FusionDrawingViewProjectCommand` | `Views 🧪` | yes (available) | yes |
| Segnaposto vista proiettata | `FusionDrawingViewProjectTemplateCommand` | `Views 🧪` | yes (available) | yes |
| Vista ausiliaria | `FusionDrawingViewAuxiliaryCommand` | `Views 🧪` | yes (available) | yes |
| Vista in sezione semplice | `FusionDrawingViewSimpleSectionCommand` | `Views 🧪` | yes (available) | yes |
| Vista in sezione | `FusionDrawingViewSectionCommand` | `Views 🧪` | yes (available) | yes |
| Vista di dettaglio | `FusionDrawingViewDetailCommand` | `Views 🧪` | yes (available) | yes |
| Vista interrotta | `FusionBrokenViewCommand` | `Views 🧪` | yes (available) | yes |
| Vista in sezione interruzione | `FusionDrawingBreakoutSectionViewCommand` | `Views 🧪` | yes (available) | yes |
| Vista di ritaglio | `FusionDrawingCropViewCommand` | `Views 🧪` | yes (available) | yes |
| Vista prospettica | `FusionDrawingViewPerspectiveCommand` | `Views 🧪` | yes (available) | yes |
| Crea schizzo | `FusionDrawingViewSketchCommand` | `DrawingSketches.add 🧪` | yes (available) | yes |
| Orizzontale/Verticale | `FDWGGcHorizontalVerticalCommand` | — | yes (available) | — |
| Coincidente | `FDWGGcCoincidentCommand` | — | yes (available) | — |
| Tangente | `FDWGGcTangentCommand` | — | yes (available) | — |
| Uguale | `FDWGGcEqualCommand` | — | yes (available) | — |
| Parallelo | `FDWGGcParallelCommand` | — | yes (available) | — |
| Perpendicolare | `FDWGGcPerpendicularCommand` | — | yes (available) | — |
| Fisso | `FDWGGcFixCommand` | — | yes (available) | — |
| Concentrico | `FDWGGcConcentricCommand` | — | yes (available) | — |
| Collineare | `FDWGGcCollinearCommand` | — | yes (available) | — |
| Simmetrico | `FDWGGcSymmetricCommand` | — | yes (available) | — |
| Offset | `FusionDrawingOffsetCommand` | — | yes (available) | — |
| Ruota | `FusionDocRotateCmd` | — | yes (available) | — |
| Ritaglia | `FusionDrawingTrimCommand` | — | yes (available) | — |
| Estendi | `FusionDrawingExtendCommand` | — | yes (available) | — |
| Sposta | `FusionDrawingMoveCmd` | — | yes (available) | — |
| Copia | `FusionDrawingCopyCommand` | — | yes (available) | — |
| Elimina | `FusionDrawingEraseCmd` | `Drawing.deleteEntities` | yes (available) | no |
| Aggiorna proprietà | `DrawingsPropertyRefreshCmd` | — | yes (available) | — |
| Linea d'asse | `FusionDrawingCenterlineCommand` | — | yes (available) | — |
| Centro | `FusionDrawingCentermarkCommand` | — | yes (available) | — |
| Serie centrata | `FusionDrawingCenterPatternCommand` | — | yes (available) | — |
| Estensione spigolo | `FusionDrawingEdgeExtensionCmd` | — | yes (available) | — |
| Quota | `FusionDrawingSingleDimensionCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Quota automatica | `FusionDrawingAutoDimensionCommand` | — | yes (available) | — |
| Riordina | `FusionDrawingTidyUpCommand` | — | yes (available) | — |
| Quota coordinata | `FusionDrawingOrdinateDimensionCmd` | — | yes (available) | — |
| Cambia impostazioni di automazione | `FusionDocAutomationSettingsCmd` | `DocumentSettings 🧪` | yes (available) | yes |
| Quota lineare | `FusionDrawingLinearDimensionCmd` | `DrawingDimensions.addLinearDimension 🧪` | yes (available) | yes |
| Quota allineata | `FusionDrawingAlignedDimensionCmd` | `DrawingDimensions.addLinearDimension 🧪` | yes (available) | yes |
| Quota angolare | `FusionDrawingAngularDimensionCmd` | `DrawingDimensions.addAngularDimension 🧪` | yes (available) | no |
| Quota raggio | `FusionDrawingRadialDimensionCmd` | `DrawingDimensions.addRadialDimension 🧪` | yes (available) | yes |
| Quota diametro | `FusionDrawingDiameterDimensionCmd` | `DrawingDimensions.addDiameterDimension 🧪` | yes (available) | yes |
| Quota radiale ridotta | `FusionDrawingJoggedRadiusDimensionCmd` | `DrawingDimensions.addJoggedRadiusDimension 🧪` | yes (available) | no |
| Quota lunghezza arco | `FusionDrawingArcDimensionCmd` | `DrawingDimensions.addArcLengthDimension 🧪` | yes (available) | no |
| Quota max min. curva | `FusionDocMinMaxDimensionCmd` | — | yes (available) | — |
| Quota linea di base | `FusionDrawingBaselineDimensionCmd` | — | yes (available) | — |
| Quota in serie | `FusionDrawingChainDimensionCmd` | — | yes (available) | — |
| Disponi quote | `FusionDrawingDimensionArrangeCmd` | — | yes (available) | — |
| Accoppia quota | `FusionDrawingMatchDimensionCmd` | — | yes (available) | — |
| Inverti frecce | `FusionDrawingFlipDimArrowCmd` | — | yes (available) | — |
| Interruzione quota | `FusionDrawingDimensionBreakCmd` | — | yes (available) | — |
| Sostituisci con aspetto configurato | `FusionDrawingReplaceDimensionWithConfigAspectCmd` | `DrawingDimensions 🧪` | configurations: no | yes |
| Testo | `FusionDrawingMTextCommand` | — | yes (available) | — |
| Nota | `FusionDrawingNoteCommand` | — | yes (available) | — |
| Nota direttrice | `FusionDrawingLeaderCommand` | — | yes (available) | — |
| Nota su foro e filettatura | `FusionDrawingHoleThreadNoteLeaderCommand` | — | yes (available) | — |
| Nota piega | `FusionDrawingBendNoteLeaderCommand` | — | yes (available) | — |
| Attributo | `FusionDrawingAttDefCommand` | — | yes (available) | — |
| Stato della superficie | `FusionDrawingSurfaceTextureCmd` | — | yes (available) | — |
| Riquadro di controllo della geometria | `FusionDrawingFeatureControlFrameCmd` | `DrawingSymbols.addFeatureControlFrame 🧪` | yes (available) | yes |
| Identificatore del riferimento | `FusionDrawingDatumIdCmd` | `DrawingSymbols.addDatumIdentifier 🧪` | yes (available) | yes |
| Saldatura | `FusionDrawingWeldSymbolCmd` | — | yes (available) | — |
| Rastremazione e inclinazione | `FusionDrawingTaperSlopeSymbolCmd` | `DrawingSymbols.addTaperSlopeSymbol 🧪` | yes (available) | no |
| Simbolo spigolo | `FusionDrawingEdgeSymbolCmd` | `DrawingSymbols.addEdgeSymbol 🧪` | yes (available) | no |
| Gestisci simboli di schizzo | `FusionDrawingManageSketchSymbolCmd` | — | yes (available) | — |
| Inserisci simbolo di schizzo | `FusionDrawingInsertSketchSymbolCmd` | — | yes (available) | — |
| Crea simbolo di schizzo | `FusionDrawingCreateSketchSymbolCmd` | — | yes (available) | — |
| Inserisci immagine | `FusionDrawingImageInsertCommand` | `Images.insert 🧪` | yes (available) | yes |
| Immagine | `FusionDrawingBlockEditorImageInsertCommand` | `Images.insert 🧪` | yes (available) | yes |
| Inserisci immagine | `FusionDrawingTemplateImageInsertCommand` | `Images.insert 🧪` | yes (available) | yes |
| Elenco parti | `FusionDrawingCreatePartsListCommand` | — | yes (available) | — |
| Tabella | `FusionDrawingNewTableCommand` | `CustomTables.add 🧪` | yes (available) | yes |
| Segnaposto tabella | `FusionDrawingNewTableTemplateCommand` | — | yes (available) | — |
| Tabella personalizzata | `FusionDrawingEmptyTableCommand` | `CustomTables.add 🧪` | yes (available) | yes |
| Elenco parti | `FusionDrawingPartsListTableCommand` | — | yes (available) | — |
| Numero di riferimento | `FusionDrawingBalloonCommand` | — | yes (available) | — |
| Tabella di piega | `FusionDrawingBendTableCommand` | `BendTables 🧪` | yes (available) | no |
| Identificatore di piega | `FusionDrawingBendIDCommand` | — | yes (available) | — |
| Tabella fori | `FusionDrawingHoleTableCommand` | `HoleTables 🧪` | yes (available) | yes |
| Tabella di configurazione | `FusionDrawingConfigTableCommand` | — | configurations: no | — |
| Cronologia revisioni | `FusionDrawingRevisionTableCommand` | `RevisionTable 🧪` | yes (available) | no |
| Contrassegno di revisione | `FusionDrawingRevMarkerCommand` | — | yes (available) | — |
| Fumetto di revisione | `FusionDocRevCloudCommand` | — | yes (available) | — |
| Rinumera | `FusionDrawingRenumberCommand` | — | yes (available) | — |
| Allinea numeri di riferimento | `FusionDrawingAlignBalloonCommand` | — | yes (available) | — |
| Preferenze di automazione | `DrawingAutomationPreferenceCmd` | `AutomationPreferences 🧪` | yes (available) | no |
| Termina cartiglio | `FusionDrawingBlockCloseCommand` | — | yes (available) | — |
| Termina bordo | `FusionDrawingBorderCloseCommand` | — | yes (available) | — |
| Termina schizzo | `FusionDrawingSketchCloseCommand` | — | yes (available) | — |
| Termina simbolo di schizzo | `FusionDrawingSketchSymbolCloseCommand` | — | yes (available) | — |
| Termina schizzo | `FusionDrawingViewSketchCloseCommand` | — | yes (available) | — |
| Esporta PDF | `FusionDrawingExportPDFCommand` | `DrawingExportManager.createPDFExportOptions` | yes (available) | yes |
| Esporta DWG | `ExportFusionDrawingDocumentCommand` | `DrawingExportManager.createDWGExportOptions` | yes (available) | yes |
| Esporta foglio come DXF | `FusionDrawingExportDXFCommand` | `DrawingExportManager.createDXFExportOptions` | yes (available) | no |
| Modello di disegno di output | `ExportFusionDrawingTemplateCommand` | — | yes (available) | — |
| Esporta CSV | `FusionDrawingExportPartsListCommand` | — | yes (available) | — |
| Debug del disegno | `FusionDrawingDebugCommand` | — | yes (available) | — |
| Riepilogo modifiche | `DrawingShowChangeAwarenessToolbarCmd` | — | yes (available) | — |
| Misura | `FusionDrawingMeasureCommand` | — | yes (available) | — |
| Cronologia | `FusionDocShowHistoryForDrawingToolbarCommand` | — | yes (available) | — |

## Drawing / COMPONENTI ELETTRONICI tab (`ElectronicsTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Vista pila di layer | `ECADLayerStackDiagramCmd` | — | electronics: separate skill | — |
| Vista rame | `ECADCopperViewCmd` | — | electronics: separate skill | — |
| Vista forature | `ECADDrillViewCmd` | — | electronics: separate skill | — |
| Tabella Pila di layer | `LayerStackTableCmd` | — | electronics: separate skill | — |
| Tabella forature | `ECADDrillTableCmd` | — | electronics: separate skill | — |

## Drawing / GESTISCI tab (`ManageTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Aggiorna | `ManageExtRefreshCmd` | — | yes (available) | — |

## Drawing / CARTIGLIO tab (`TitleBlockTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Linea | `FusionDrawingLineCommand` | `DrawingSketch.lines 🧪` | yes (available) | yes |
| Rettangolo mediante 2 punti | `FusionDrawingRectangleCommand` | `DrawingSketch.rectangles 🧪` | yes (available) | no |
| Cerchio centro-raggio | `FusionDrawingCircleCommand` | `DrawingSketch.circles 🧪` | yes (available) | no |
| Ellisse | `FusionDrawingEllipseCommand` | `DrawingSketch.ellipses 🧪` | yes (available) | no |
| Arco a 3 punti | `FusionDrawingArcCommand` | `DrawingSketch.arcs 🧪` | yes (available) | yes |
| Direttrice | `FusionDrawingArrowCommand` | — | yes (available) | — |
| Etichetta | `FusionDrawingLabelDefCommand` | — | yes (available) | — |
| Quota dello schizzo | `FDWGSketchSmartConstarintDimCommand` | — | yes (available) | — |

## Drawing / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Riassocia | `FusionDrawingDimReassociateCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Elimina vincolo | `FusionDocDeleteConstraintCmd` | — | yes (available) | — |
| Riassocia | `FusionDrawingSmartObjReassociateCmd` | — | yes (available) | — |
| Riassocia | `FusionDrawingCustomLeaderReassociateCmd` | — | yes (available) | — |
| Continua | `FusionDrawingContinueCmd` | — | yes (available) | — |
| Annulla | `CancelCommand` | — | yes (available) | — |
| Modifica vista | `FusionDrawingViewEditCommand` | `Views 🧪` | yes (available) | yes |
| Annulla | `FusionDrawingUndoCommand` | — | yes (available) | — |
| Ripeti | `FusionDrawingRedoCommand` | — | yes (available) | — |
| Modifica impostazioni documento | `FusionChangeMultiDocSettingCommand` | — | yes (available) | — |
| FusionChangeDocumentSettingsCommand | `FusionChangeDocumentSettingsCommand` | `Documents.add` | yes (available) | yes |
| Modifica impostazioni documento | `FusionChangeDocSettingCommand` | `DocumentSettings 🧪` | yes (available) | yes |
| Importa impostazioni documento | `FusionImportDocSettingsCommand` | `Documents.add` | yes (available) | yes |
| Modifica font | `FusionChangeFontCommand` | — | yes (available) | — |
| Modifica gruppo altezza testo | `FusionChangeTextHeightGroupCommand` | — | yes (available) | — |
| Modifica gruppo larghezza linea | `FusionChangeLineWidthGroupCommand` | — | yes (available) | — |
| Modifica unità di quota | `FusionChangeDimensionUnitsCommand` | `DocumentSettings 🧪` | yes (available) | yes |
| Modifica ambito revisione | `FusionChangeRevisionScopeCommand` | — | yes (available) | — |
| Modifica impostazioni foglio | `FusionChangeMultiSheetSettingsCommand` | — | yes (available) | — |
| Modifica dimensioni foglio | `FusionChangeSheetSizeCommand` | `DocumentSettings 🧪` | yes (available) | yes |
| Modifica cartiglio | `FusionChangeTitleBlockCommand` | `TitleBlocks 🧪` | yes (available) | yes |
| Modifica visualizzazione bordo | `FusionChangeDisplayBorderCommand` | `Viewport.camera` | yes (available) | yes |
| Modifica visualizzazione cartiglio | `FusionChangeDisplayTitleBlockCommand` | `TitleBlocks 🧪` | yes (available) | yes |
| Apri | `OpenRelatedDesignCommand` | `Documents.add` | yes (available) | yes |
| Reimposta | `FusionDocRestoreDefaultsCmd` | — | yes (available) | — |
| Mostra in posizione | `ShowInLocationDrawingCmd` | — | yes (available) | no |
| Impila quote | `FusionDrawingDimensionStackArrangeCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Allinea quote | `FusionDrawingDimensionAlignArrangeCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Accoppia quota | `FusionDrawingMatchDimCntxMenuCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Inverti frecce | `FusionDrawingFlipDimArrowCntxMenuCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Aggiungi interruzione quota | `FusionDrawingAddDimensionBreakCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Rimuovi interruzione quota | `FusionDrawingRemoveDimensionBreakCmd` | `DrawingDimensions 🧪` | yes (available) | yes |
| Cambia configurazione | `SwitchConfigurationCommand` | — | configurations: no | — |
| Sostituisci con aspetto configurato | `FusionDrawingReplaceDimensionWithConfigAspectContextMenuCmd` | `DrawingDimensions 🧪` | configurations: no | yes |
| Modifica vista di ritaglio | `FusionDrawingCropViewEditCommand` | `Views 🧪` | yes (available) | yes |
| Mostra/nascondi Contorno di ritaglio | `FusionDrawingCropOutlineCommand` | `Views 🧪` | yes (available) | yes |
| Modifica bordo | `FusionDrawingBorderEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Mostra/Nascondi | `FusionChangeBorderVisibilityCommand` | — | yes (available) | no |
| Nuovo cartiglio | `FusionDrawingNewTitleBlockCommand` | `TitleBlocks 🧪` | yes (available) | yes |
| Modifica cartiglio | `FusionDrawingBlockEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica proprietà | `FusionEditPropertiesCommand` | — | yes (available) | — |
| Ripristina proprietà | `FusionResetPropertiesCommand` | — | yes (available) | — |
| Mostra/Nascondi | `FusionChangeTitleBlockVisibilityCommand` | `TitleBlocks 🧪` | yes (available) | yes |
| Modifica schizzo | `FusionDrawingSketchEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Modifica schizzo | `FusionDrawingViewSketchEditCommand` | `Views 🧪` | yes (available) | yes |
| Modifica quote automatiche | `FusionDrawingAutoDimensionEditCommand` | `DrawingDimensions 🧪` | yes (available) | yes |
| Ottieni quota alternativa | `FusDocGetAlternateDimCommand` | — | yes (available) | — |
| FusDocGetAlternatePointCommand | `FusDocGetAlternatePointCommand` | — | yes (available) | — |
| Taglia | `FusionDocCutSketchCommand` | — | yes (available) | — |
| Copia | `FusionDocCopySketchCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteSketchCommand` | — | yes (available) | — |
| Taglia | `FusionDocCutGeomEntityCommand` | — | yes (available) | — |
| Copia | `FusionDocCopyGeomEntityCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteGeomEntityCommand` | — | yes (available) | — |
| Taglia | `FusionDocCutMtextCommand` | — | yes (available) | — |
| Copia | `FusionDocCopyMtextCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteTextCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteCustomMTextCommand` | — | yes (available) | — |
| Copia | `FusionDocCopyCustomTableCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteCustomTableCommand` | — | yes (available) | — |
| Incolla | `FusionDocPasteExternalCustomTableCommand` | — | yes (available) | — |
| Elimina | `FusionDocDeleteCmd` | `Drawing.deleteEntities` | yes (available) | no |
| Elimina | `FusionDrawingSketchDeleteCommand` | — | yes (available) | — |
| Mostra/Nascondi | `SketchShowHideCommand` | — | yes (available) | no |
| Mostra/Nascondi | `FusionDrawingShowHideCommand` | — | yes (available) | no |
| FusionDrawingShowHideSketchesSketchCommand | `FusionDrawingShowHideSketchesSketchCommand` | — | yes (available) | no |
| Mostra tutti i componenti | `FusionDrawingShowAllChildCommand` | — | yes (available) | no |
| Mostra tutti i componenti | `FusionDrawingShowAllCommand` | — | yes (available) | no |
| Scopri tutti i componenti | `FusionDrawingUnsuppressAllCommand` | — | yes (available) | — |
| Cronologia progetto | `FusionDocShowHistoryForDesignCommand` | — | yes (available) | no |
| Disegni precedenti | `FusionDocShowHistoryForDrawingCommand` | — | yes (available) | no |
| Modifica proprietà modello | `FusionDocModelPropertyEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |
| Sopprimi | `FusionDrawingSuppressCommand` | — | yes (available) | — |
| Scopri | `FusionDrawingUnsuppressCommand` | — | yes (available) | — |
| Scopri tutti i componenti | `FusionDrawingUnsuppressAllChildCommand` | — | yes (available) | — |
| Sopprimi tutto eccetto i selezionati | `FusionDrawingSuppressAllExceptSelectedCommand` | `Selections` | yes (available) | no |
| Aggiorna | `FusionDrawingUpdateLinkTable` | — | yes (available) | — |
| Interrompi | `FusionDrawingBreakLinkTable` | — | yes (available) | — |
| Modifica vista in sezione interruzione | `FusionDrawingBreakoutSectionViewEditCommand` | `Views 🧪` | yes (available) | yes |

## Rendering / RENDERING tab (`RenderTab`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Visualizzazione AI | `AIVisualizationCommand` | — | consumes tokens: not without a request | — |
| Impostazioni scena | `RenderingEnvCmd` | `RenderManager.sceneSettings` | yes (available) | yes |
| Luce | `LightCommand` | `Lights 🧪` | yes (available) | no |
| Controlli della mappa di texture | `TextureMappingCommand` | `TextureMapControl` | yes (available) | no |
| Controllo priorità dielettrica | `DielectricPriorityControlCmd` | — | yes (available) | — |
| Rendering su area graf. | `InCanvasRenderCommand` | `RenderManager.inCanvasRendering` | yes (available) | no |
| Impostazioni di rendering su area grafica | `InCanvasRenderSettingsCommand` | `RenderManager.inCanvasRendering` | yes (available) | no |
| Cattura immagine... | `SaveAsImageCommand` | `Viewport.saveAsImageFile` | yes (available) | yes |
| Rendering | `A360RenderCommand` | `RenderManager.rendering` | yes (available) | yes |

## Rendering / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Sopprimi | `SuppressNamedLightCmd` | `Light.isSuppressed 🧪` | yes (available) | yes |
| Sopprimi tutto | `SuppressAllNamedLightsCmd` | `Light.isSuppressed 🧪` | yes (available) | yes |
| Scopri | `UnsuppressNamedLightCmd` | `Light.isSuppressed 🧪` | yes (available) | yes |
| Scopri tutto | `UnsuppressAllNamedLightsCmd` | `Light.isSuppressed 🧪` | yes (available) | yes |

## Animation / ANIMAZIONE tab (`Animation`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Nuovo storyboard | `PublisherCreateStoryboardCommand` | `Storyboards.add` | yes (available) | yes |
| Trasforma componenti | `PublisherMoveComponentsCommand` | — | yes (available) | — |
| Ripristina posizione iniziale | `PublisherRestoreHomeCommand` | — | yes (available) | — |
| Esplosione automatica: un livello | `PublisherExplodeDirectChildrenCommand` | — | yes (available) | — |
| Esplosione automatica: tutti i livelli | `PublisherExplodeAllPartsCommand` | — | yes (available) | — |
| Esplosione manuale | `PublisherManualExplodeCommand` | — | yes (available) | — |
| Mostra/Nascondi | `PublisherVisibilityToggleCmd` | — | yes (available) | — |
| Aspetto | `PublisherAppearanceCommand` | `Appearances` | yes (available) | yes |
| Visualizza | `PublisherToggleCameraRecordingCmd` | `Storyboard.isViewRecordingOn` | yes (available) | no |
| Pubblica video | `ExportVideoCommand` | — | yes (available) | — |

## Animation / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| PublisherEditStoryboardCmd | `PublisherEditStoryboardCmd` | `Storyboards` | yes (available) | yes |
| Inverti | `ReverseSequenceEntryCmd` | — | yes (available) | — |
| Copia | `PublisherCopyCommand` | — | yes (available) | — |
| Incolla | `PublisherPasteCommand` | — | yes (available) | — |
| Durata | `PublisherDurationCmd` | — | yes (available) | — |
| Modifica inizio/fine | `PublisherEditActionCmd` | — | yes (available) | — |
| Modifica azione | `PublisherEditTransformActionCommand` | — | yes (available) | — |
| Modifica inizio | `PublisherEditSmartObjectActionCmd` | — | yes (available) | — |
| Elimina | `PublisherDeleteCommand` | — | yes (available) | — |
| Crea richiamo | `CalloutCommand` | — | yes (available) | — |
| Attiva/disattiva materiale | `PublisherMaterialToggleCommand` | — | yes (available) | no |
| Modifica ambito materiale | `PublisherScopeMaterialCommand` | — | yes (available) | — |
| Mostra/nascondi linee finali | `PublisherTrailVisibilityCommand` | — | yes (available) | no |
| Mostra tutte le linee finali | `PublisherTrailShowAllCommand` | — | yes (available) | no |
| Nascondi tutte le linee finali | `PublisherTrailHideAllCommand` | — | yes (available) | no |
| PublisherUpdateCmd | `PublisherUpdateCmd` | — | yes (available) | — |
| Crea gruppo di selezione | `PublisherCreateSelectionGroupCmd` | `Selections` | yes (available) | no |
| Isola | `PublisherIsolateCmd` | — | yes (available) | no |
| Annulla isolamento | `PublisherUnisolateCmd` | — | yes (available) | — |
| Rinomina | `RenameStoryboardShellCmd` | — | yes (available) | — |
| Allinea ora di inizio | `AlignActionStartTimesCmd` | — | yes (available) | — |
| Allinea ora di fine | `AlignActionEndTimesCmd` | — | yes (available) | — |
| Seleziona tutti dopo | `SelectAllAfterCmd` | `Selections` | yes (available) | no |
| Seleziona tutti prima | `SelectAllBeforeCmd` | `Selections` | yes (available) | no |
| Espandi | `PublisherExpandCompositeActionsCmd` | — | yes (available) | — |
| Elimina azioni | `PublisherDeleteActorCommand` | — | yes (available) | — |
| Trova nel browser | `PublisherFindInBrowser` | — | yes (available) | — |
| Trova nella finestra | `PublisherFindInWindow` | — | nesting: paid extension — to be verified | — |
| Modifica richiamo | `CalloutEditCommand` | `TimelineObject.rollTo` | yes (available) | yes |

## Common (File menu and fixed toolbars) / Menus (File, fixed toolbars, right-click, radial) (`Menu`)

| Italian UI name | Identifier | API | Personal | Tested |
|---|---|---|---|---|
| Mostra comandi di testo | `ShowTextCommandsCommand` | — | yes (available) | no |
| Mostra Home | `ShowFusionHomeCmd` | — | yes (available) | no |
| Nascondi pannello dati | `DashboardModeSwitchCommand` | — | yes (available) | — |
| File | `FileSubMenuCommand` | `Documents.add` | yes (available) | yes |
| Nuovo... | `NewDocumentCommand` | `Documents.add` | yes (available) | yes |
| Nuovo disegno | `NewDrawingMenuCommand` | `Documents.add` | yes (available) | yes |
| Dal progetto | `NewFusionDrawingDocumentCommand` | `Documents.add` | yes (available) | yes |
| Dal progetto | `ECADNewDrawingDocumentCommand` | `Documents.add` | yes (available) | yes |
| Dal progetto | `ECADNewDrawingFromPCB3dCommand` | `Documents.add` | yes (available) | yes |
| Da animazione | `PublisherNewDrawingDocumentCommand` | `Documents.add` | yes (available) | yes |
| Nuovo modello di disegno | `NewFusionDrawingTemplateCommand` | `Documents.add` | yes (available) | yes |
| Apri... | `OpenCommand` | `Documents.add` | yes (available) | yes |
| Documenti recuperati aperti (0) | `NotifyAutoSaveFilesCommand` | `Documents.add` | yes (available) | yes |
| Carica... | `UploadCommand` | `Documents.add` | yes (available) | yes |
| Salva | `PLM360SaveCommand` | `Documents.add` | yes (available) | yes |
| Salva con nome | `PLM360SaveAsCommand` | `Documents.add` | yes (available) | yes |
| Salva come più recente | `PLM360SaveAsLatestOnQATCommand` | `Documents.add` | yes (available) | yes |
| Salva stato calcolato | `SaveComputedStateCommand` | `Documents.add` | yes (available) | yes |
| Esporta... | `ExportCommand` | `Documents.add` | yes (available) | yes |
| Crea versione | `CreateVersionCommand` | `Document.save` | yes (available) | yes |
| Stampa... | `FusionDrawingPrintCommand` | `Documents.add` | yes (available) | yes |
| Condividi collegamento file | `SimpleSharingPublicLinkCommand` | — | yes (available) | — |
| Visualizza dettagli sul Web | `PLM360OpenDetailsCommand` | `Documents.add` | yes (available) | yes |
| Visualizza | `ViewWidgetCommand` | `Viewport.camera` | yes (available) | yes |
| Nascondi ViewCube | `HideViewCubeCommand` | `Viewport.camera` | yes (available) | yes |
| Mostra ViewCube | `ShowViewCubeCommand` | `Viewport.camera` | yes (available) | yes |
| Nascondi browser | `HideBrowserCommand` | — | yes (available) | no |
| Mostra browser | `ShowBrowserCommand` | — | yes (available) | no |
| Nascondi commenti | `HideActivityFeedCommand` | — | yes (available) | no |
| Mostra commenti | `ShowActivityFeedCommand` | — | yes (available) | no |
| Nascondi tavolozza comandi | `HideCommandPaletteCommand` | — | yes (available) | no |
| Mostra tavolozza dei comandi | `ShowCommandPaletteCommand` | — | yes (available) | no |
| Nascondi comandi di testo | `HideTextCommandsCommand` | — | yes (available) | no |
| Nascondi barra di navigazione | `HideNavigationToolbarCommand` | — | yes (available) | no |
| Mostra barra di navigazione | `ShowNavigationToolbarCommand` | — | yes (available) | no |
| Nascondi barra degli strumenti dei comandi | `HideCommandToolbarCommand` | — | yes (available) | no |
| Mostra barra degli strumenti dei comandi | `ShowCommandToolbarCommand` | — | yes (available) | no |
| Mostra pannello dati | `DashboardModeOpenCommand` | `Documents.add` | yes (available) | yes |
| Nascondi pannello dati | `DashboardModeCloseCommand` | `Documents.add` | yes (available) | yes |
| Nascondi sovrapposizione prestazioni | `HidePerformanceOverlayCommand` | — | yes (available) | no |
| Mostra sovrapposizione prestazioni | `ShowPerformanceOverlayCommand` | — | yes (available) | no |
| Ripristina layout di default | `ResetToDefaultLayoutCommand` | — | yes (available) | — |
| Apri... | `OpenDocumentCommand` | `Documents.add` | yes (available) | yes |
| Salva localmente | `SaveDocumentCommand` | `Documents.add` | yes (available) | yes |
| Annulla più volte | `UndoDropDown` | — | yes (available) | — |
| Annulla | `DoraUndoCommand` | — | yes (available) | — |
| Ripeti più volte | `RedoDropDown` | — | yes (available) | — |
| Ripeti | `DoraRedoCommand` | — | yes (available) | — |
| Mostra NTest | `NTestExcMetaCommand` | — | yes (available) | — |
| Consapevolezza modifiche utente | `ShowChangeAwarenessQATCmd` | — | yes (available) | no |
| Orbita | `OrbitCommand` | `Viewport.camera` | yes (available) | yes |
| Ingrandisci finestra | `ZoomFitCommandGroup` | `Viewport.camera` | nesting: paid extension — to be verified | yes |
| Impostazioni di visualizzazione | `ViewDisplayCommand` | `Viewport.camera` | yes (available) | yes |
| Stile di visualizzazione | `ViewVisualStyleCommand` | `Viewport.camera` | yes (available) | yes |
| Ambiente | `ViewEnvCommand` | `Viewport.camera` | yes (available) | yes |
| Preset grafica | `ViewGraphicsPresetCommand` | `Viewport.camera` | yes (available) | yes |
| Effetti | `ViewEffectCommand` | `Viewport.camera` | yes (available) | yes |
| Visibilità oggetto | `VisibilityOverrideCommand` | — | yes (available) | no |
| Inquadratura | `ViewCameraCommand` | `Viewport.camera` | yes (available) | yes |
| Stile di visualizzazione | `SplitViewVisualStyleCommand` | `Viewport.camera` | yes (available) | yes |
| Inquadratura | `SplitViewCameraCommand` | `Viewport.camera` | yes (available) | yes |
| Offset del piano di base | `GroundPlaneOffsetCommand` | `Design.setGroundPlaneOffset` | yes (available) | no |
| Attiva modalità schermo intero | `ShowWorkspaceFullScreenCommand` | — | yes (available) | no |
| Esci dalla modalità schermo intero | `ShowWorkspaceNormalCommand` | — | yes (available) | no |
| Griglia e snap | `ViewLayoutGridCommand` | `Viewport.camera` | yes (available) | yes |
| Impostazioni griglia | `DefineGridCmd` | `Viewport.camera` | yes (available) | yes |
| Spostamento incrementale | `ToggleIncrementalMoveCmd` | — | yes (available) | no |
| Imposta incrementi | `SetSnapValueCmd` | `Viewport.camera` | yes (available) | yes |
| Finestre | `SplitViewWindowSyncCommand` | `Viewport.camera` | nesting: paid extension — to be verified | yes |
| Vista singola | `SingleViewCmd` | `Viewport.camera` | yes (available) | yes |
| Viste multiple | `MultiViewCmd` | `Viewport.camera` | yes (available) | yes |
| Reimposta viste | `SplitViewResetCmd` | `Viewport.camera` | yes (available) | yes |
| Accesso di base | `BasicAccessCommand` | — | yes (available) | — |
| 0 E - 0 W | `HealthStatusCommand` | — | yes (available) | — |
| Scaduto: abbonati subito | `TryToBuyCommand` | — | yes (available) | — |
| Aggiorna ad un abbonamento a Fusion | `RequestTrialCommand` | — | yes (available) | — |
| ConnectivityStatusCommand | `ConnectivityStatusCommand` | — | yes (available) | — |
| Manutenzione del servizio cloud. | `CloudServiceStatusCommand` | — | yes (available) | — |
| UpdateAvailableCommand | `UpdateAvailableCommand` | — | yes (available) | — |
| NotificationCommand | `NotificationCommand` | — | yes (available) | — |
| Autodesk Assistant | `AANewChatCommand` | `Documents.add` | yes (available) | yes |
| FeaturePacksCommand | `FeaturePacksCommand` | — | yes (available) | — |
| CloudStatusCommand | `CloudStatusCommand` | — | yes (available) | — |
| Centro notifiche | `NotificationCenterCommand` | — | yes (available) | — |
| Subscription | `SubscriptionCommand` | — | yes (available) | — |
| Guida | `HelpGroupCommand` | — | yes (available) | — |
| Apprendimento e documentazione | `LearningAndHelpCommand` | — | yes (available) | — |
| Apprendimento personalizzato | `HelpCommand` | — | yes (available) | — |
| Documentazione del prodotto | `LearningAndTutorialsCommand` | — | yes (available) | — |
| Impostazione rapida | `LearningPaletteCommand` | — | yes (available) | — |
| Autodesk Assistant | `AAChatCommand` | — | yes (available) | — |
| Comunità | `CommunityCommand` | — | yes (available) | — |
| Forum | `ForumCommand` | — | yes (available) | — |
| Programma Insider | `SubmitAnIdeaCommand` | — | yes (available) | — |
| Blog | `BlogCommand` | — | yes (available) | — |
| Supporto e diagnostica | `SupportAndDiagnosticsCommand` | — | yes (available) | — |
| Ottieni supporto | `FeedbackCommand` | — | yes (available) | — |
| Annota file di registro | `AnnotateLogFileCommand` | `Documents.add` | yes (available) | yes |
| File di registro di diagnostica | `GatherDiagnosticsDataCommand` | — | yes (available) | — |
| Diagnostica grafica | `GraphicsDiagnosticsCommand` | — | yes (available) | — |
| Cancella dati cache | `ClearUserCacheCommand` | — | yes (available) | — |
| Service Utility | `ServiceUtilityCommand` | — | yes (available) | — |
| Segnala problemi di prestazioni | `PerfFeedbackRecorderCmd` | — | yes (available) | — |
| Entra in contatto con un esperto | `StreetTeamCommand` | — | yes (available) | — |
| Invia feedback | `PreReleaseFeedbackCommand` | — | bill of materials and releases (Manage): no | — |
| Segnala un problema | `ReportProblemCmd` | — | yes (available) | — |
| Verifica aggiornamenti | `UpdateNowCommand` | — | yes (available) | — |
| Novità | `WhatsNewCommand` | `Documents.add` | yes (available) | yes |
| Note di rilascio | `ReleaseNotesCommand` | — | bill of materials and releases (Manage): no | — |
| Informazioni | `AboutBoxCommand` | — | yes (available) | — |
| Esercitazioni | `TutorialsCommand` | — | yes (available) | — |
| Riferimento rapido | `QuickStartCommand` | — | yes (available) | — |
| Video sulle caratteristiche essenziali | `VideosCommand` | — | yes (available) | — |
| CIPCommand | `CIPCommand` | — | yes (available) | — |
| Nessun utente ha eseguito il login | `UserDisplayNameCommand` | `Viewport.camera` | yes (available) | yes |
| Autodesk Account | `GoToMyAccountCommand` | — | yes (available) | — |
| Preferenze | `PreferencesCommand` | `Preferences` | yes (available) | no |
| Scelte rapide dei comandi | `CommandShortcutsManagerCommand` | — | yes (available) | — |
| Cambia team | `UserHubsCommand` | — | yes (available) | — |
| Profilo personale | `GoToMyProfileCommand` | — | yes (available) | — |
| Cloud personale | `MyCloudCommand` | — | yes (available) | — |
| Condividi commenti | `ShareFeedbackCommand` | — | yes (available) | — |
| Abbonati subito | `SubscribeNowCommand` | — | yes (available) | — |
| Esci | `QontextLogoutCommand` | — | yes (available) | — |
| Avviso | `AlertCommand` | — | yes (available) | — |
| CommentiPerf | `PerformanceFeedbackCommand` | — | yes (available) | — |
| Autodesk Assistant | `ChatCommand` | — | yes (available) | — |
| ActiveDocumentAction | `ActiveDocumentAction` | `Documents.add` | yes (available) | yes |
