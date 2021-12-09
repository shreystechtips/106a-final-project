import React, { useEffect, useState } from "react";
import CanvasDraw from "react-canvas-draw";

import { Grid, Button } from "@mui/material";

function App() {
	const size = useWindowSize();
	const padding = 10;
	const width = window.innerWidth - padding * 2;
	const height = window.innerHeight - padding * 2;
	// const staticSize = Math.min(
	// 	(Math.max(window.innerWidth , window.innerHeight) * 2) / 3,
	// 	Math.min(window.innerWidth, window.innerHeight)
	// );
	const staticSize = Math.min(
		(Math.max(width, height) * 2) / 3,
		Math.min(width, height)
	);

	var canvas = null;
	return (
		<Grid
			container
			spacing={10}
			direction="row"
			justifyContent="space-evenly"
			alignItems="flex-start"
			style={{
				padding: padding,
			}}
		>
			<Grid item>
				{size === null ? (
					<></>
				) : (
					<CanvasDraw
						style={{
							boxShadow:
								"0 13px 27px -5px rgba(50, 50, 93, 0.25),    0 8px 16px -8px rgba(0, 0, 0, 0.3)",
						}}
						ref={(canvasDraw) => (canvas = canvasDraw)}
						lazyRadius={0}
						canvasWidth={staticSize}
						canvasHeight={staticSize}
					/>
				)}
			</Grid>
			<Grid item>
				<Grid container direction="column" spacing={5}>
					<Grid item>
						<Button
							variant="contained"
							onClick={() => {
								console.log(canvas.getSaveData());
							}}
						>
							Draw!
						</Button>
					</Grid>
					<Grid item>
						<Button
							variant="contained"
							onClick={() => {
								if (canvas != null) {
									canvas.eraseAll();
								}
							}}
						>
							Reset
						</Button>
					</Grid>
				</Grid>
			</Grid>
		</Grid>
	);
}

function useWindowSize() {
	// Initialize state with undefined width/height so server and client renders match
	// Learn more here: https://joshwcomeau.com/react/the-perils-of-rehydration/
	const [windowSize, setWindowSize] = useState(0);
	useEffect(() => {
		// Handler to call on window resize
		function handleResize() {
			// Set window width/height to state
			const big = (Math.max(window.innerWidth, window.innerHeight) * 2) / 3;
			const small = Math.min(window.innerWidth, window.innerHeight);
			setWindowSize(Math.min(big, small));
		}
		// Add event listener
		window.addEventListener("resize", handleResize);
		// Call handler right away so state gets updated with initial window size
		handleResize();
		// Remove event listener on cleanup
		return () => window.removeEventListener("resize", handleResize);
	}, []); // Empty array ensures that effect is only run on mount
	return windowSize == null ? 0 : windowSize;
}

export default App;

{
	/* <h1>React-Canvas-Draw</h1>
			<h3>A simple yet powerful canvas-drawing component for React</h3>
			<iframe
				title="GitHub link"
				src="https://ghbtns.com/github-btn.html?user=embiem&repo=react-canvas-draw&type=star&count=true"
				frameborder="0"
				scrolling="0"
				width="160px"
				height="30px"
			/>
			<p>
				<span role="img" aria-label="fingers pointing down">
					👇👇👇👇
				</span>{" "}
				{/* Use your {isMobOrTab ? "finger" : "mouse"} to draw{" "} */
}
//				<span role="img" aria-label="fingers pointing down">
//				👇👇👇👇
//		</span></p>
