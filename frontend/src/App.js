import React, { useEffect, useState } from "react";
import CanvasDraw from "react-canvas-draw";

import { Grid, Button, Typography } from "@mui/material";

const API_URL = "http://192.168.0.102:5000";
const POST_URL = `${API_URL}/api/post_points`;
const PRESET_URL = `${API_URL}/api/draw_preset`;
const PROG_URL = `${API_URL}/api/get_status`;

const drawTypes = ["swirl", "demo", "cardiod", "lisajous"];

function App() {
	const size = useWindowSize();
	const padding = 10;
	const width = window.innerWidth - padding * 2;
	const height = window.innerHeight - padding * 2;
	const [prog, setProg] = useState(0);
	// const staticSize = Math.min(
	// 	(Math.max(window.innerWidth , window.innerHeight) * 2) / 3,
	// 	Math.min(window.innerWidth, window.innerHeight)
	// );
	const staticSize = Math.min(
		(Math.max(width, height) * 2) / 3,
		Math.min(width, height)
	);

	function getStat() {
		fetch(PROG_URL)
			.then((res) => {
				return res.json();
			})
			.catch((err) => {
				return { progress: 0 };
			})
			.then((data) => {
				if (prog != data.percent) {
					setProg(data.percent);
				}
			});
	}

	function draw(type) {
		console.log(type);
		fetch(PRESET_URL, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				preset: type,
				rr: 2,
				offset: 0,
			}),
		})
			.then((res) => {
				if (!res.ok) {
					throw new Error(res.statusText);
				}
				const val = res.json();
				if (val.status == "P") {
					alert("oops, in progress already");
				}
			})
			.catch((err) => alert("Error in request!"));
	}

	function sendData(data, size) {
		console.log(data, size);
		fetch(POST_URL, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				points: data.points.map((elem) => [elem.x, elem.y]),
				size: size,
			}),
		})
			.then((res) => {
				if (!res.ok) {
					throw new Error(res.statusText);
				}
				const val = res.json();
				if (val.status == "P") {
					alert("oops, in progress already");
				}
			})
			.catch((err) => alert("Error in request!"));
	}

	var canvas = null;
	return (
		<Grid
			container
			spacing={5}
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
				<Grid container direction="column" spacing={2}>
					<Grid item>
						<Button
							variant="contained"
							disabled={
								canvas === null
									? false
									: canvas.getSaveData()["lines"].length <= 0
							}
							onClick={() => {
								const data = JSON.parse(canvas.getSaveData());
								if (data.lines.length > 1) {
									let complete = window.confirm(
										"Click ok to draw the first line, cancel to not do anything"
									);
									if (!complete) {
										return;
									}
								} else if (data.lines.length === 0) {
									alert("no lines drawn, aborting");
									return;
								}
								sendData(data.lines[0], [data.width, data.height]);
							}}
							style={{
								// padding: 50,
								borderRadius: 20,
								fontSize: 40,
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
							style={{
								// padding: 50,
								borderRadius: 20,
								fontSize: 40,
							}}
						>
							Reset
						</Button>
					</Grid>
					<Grid item>
						<Button
							variant="contained"
							onClick={() => {
								if (canvas != null) {
									canvas.undo();
								}
							}}
							style={{
								// padding: 50,
								borderRadius: 20,
								fontSize: 40,
							}}
						>
							Undo
						</Button>
					</Grid>
					<Grid item>
						<Button
							variant="contained"
							onClick={getStat}
							style={{
								// padding: 50,
								borderRadius: 20,
								fontSize: 40,
							}}
						>
							Update Status
						</Button>
					</Grid>
					<Grid item>
						<Grid container direction="row" spacing={2}>
							{drawTypes.map((elem) => (
								<Grid item>
									<Button
										variant="contained"
										onClick={() => draw(elem)}
										id={elem}
									>
										{elem}
									</Button>
								</Grid>
							))}
						</Grid>
					</Grid>
					<Grid item>
						<Typography
							style={{
								// padding: 50,
								borderRadius: 20,
								fontSize: 40,
							}}
						>
							Prog: {prog}%
						</Typography>
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
